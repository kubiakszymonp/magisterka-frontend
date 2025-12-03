import React from "react";
import { marked } from "marked";

// Block elements that should be treated as sentence boundaries
const BLOCK_ELEMENTS = new Set([
  "h1", "h2", "h3", "h4", "h5", "h6",
  "p", "li", "blockquote", "div", "section", "article"
]);

// Strip markdown/HTML to get plain text for sentence detection
export function stripMarkdown(markdown: string): string {
  // Convert markdown to HTML first
  const html = marked.parse(markdown, { async: false }) as string;
  
  if (typeof window === "undefined") {
    // SSR fallback - simple regex
    return html
      .replace(/<[^>]*>/g, " ")
      .replace(/&nbsp;/g, " ")
      .replace(/&amp;/g, "&")
      .replace(/&lt;/g, "<")
      .replace(/&gt;/g, ">")
      .replace(/&quot;/g, '"')
      .replace(/&#39;/g, "'")
      .replace(/\s+/g, " ")
      .trim();
  }
  
  // Parse HTML and extract text respecting block boundaries
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, "text/html");
  
  const textParts: string[] = [];
  extractTextWithBlockBoundaries(doc.body, textParts);
  
  // Join with a sentence-ending marker
  return textParts
    .map(t => t.trim())
    .filter(t => t.length > 0)
    .join(". ")
    .replace(/\.\s*\./g, ".")
    .replace(/\s+/g, " ")
    .trim();
}

function extractTextWithBlockBoundaries(node: Node, parts: string[]): void {
  if (node.nodeType === Node.TEXT_NODE) {
    const text = node.textContent || "";
    if (text.trim()) {
      // Add to current part or create new one
      if (parts.length === 0) {
        parts.push(text);
      } else {
        parts[parts.length - 1] += text;
      }
    }
    return;
  }
  
  if (node.nodeType === Node.ELEMENT_NODE) {
    const element = node as Element;
    const tagName = element.tagName.toLowerCase();
    
    // Start new part for block elements
    if (BLOCK_ELEMENTS.has(tagName)) {
      parts.push("");
    }
    
    node.childNodes.forEach(child => {
      extractTextWithBlockBoundaries(child, parts);
    });
  }
}

// Split text into sentences
function splitIntoSentences(text: string): string[] {
  return text.split(/(?<=[.!?;:])\s+/).filter((s) => s.trim().length > 0);
}

interface HighlightedHtmlProps {
  markdown: string;
  currentSentenceIndex: number | null;
  onSentenceClick: (index: number) => void;
}

export function HighlightedHtml({
  markdown,
  currentSentenceIndex,
  onSentenceClick,
}: HighlightedHtmlProps) {
  // Convert markdown to HTML
  const html = marked.parse(markdown, { async: false }) as string;

  // Parse HTML and wrap sentences with highlight spans
  const processedHtml = wrapSentencesInHtml(
    html,
    currentSentenceIndex,
    onSentenceClick
  );

  return <>{processedHtml}</>;
}

// Context for tracking sentence matching across the document
interface MatchContext {
  globalSentenceIndex: number;
  highlightedSentenceIndex: number | null;
  onSentenceClick: (index: number) => void;
}

// Context for a single block element
interface BlockContext {
  sentences: string[];
  currentSentenceIdx: number;
  currentProgress: string;
}

// Parse HTML and wrap text content with sentence highlighting
function wrapSentencesInHtml(
  html: string,
  highlightedSentenceIndex: number | null,
  onSentenceClick: (index: number) => void
): React.ReactNode[] {
  if (typeof window === "undefined") {
    return [<span key="ssr" dangerouslySetInnerHTML={{ __html: html }} />];
  }

  const parser = new DOMParser();
  const doc = parser.parseFromString(html, "text/html");

  const context: MatchContext = {
    globalSentenceIndex: 0,
    highlightedSentenceIndex,
    onSentenceClick,
  };

  const result = processNode(doc.body, "root", context, null);
  return Array.isArray(result) ? result : [result];
}

// Extract plain text from a node for sentence splitting
function extractPlainText(node: Node): string {
  if (node.nodeType === Node.TEXT_NODE) {
    return node.textContent || "";
  }
  if (node.nodeType === Node.ELEMENT_NODE) {
    let text = "";
    node.childNodes.forEach(child => {
      text += extractPlainText(child);
    });
    return text;
  }
  return "";
}

function processNode(
  node: Node,
  keyPrefix: string,
  context: MatchContext,
  blockContext: BlockContext | null
): React.ReactNode {
  if (node.nodeType === Node.TEXT_NODE) {
    if (!blockContext) {
      return node.textContent;
    }
    return processTextNode(node.textContent || "", keyPrefix, context, blockContext);
  }

  if (node.nodeType === Node.ELEMENT_NODE) {
    const element = node as Element;
    const tagName = element.tagName.toLowerCase();
    
    // Check if this is a block element that starts new sentences
    const isBlockElement = BLOCK_ELEMENTS.has(tagName);
    
    // Create new block context for block elements
    let newBlockContext = blockContext;
    if (isBlockElement) {
      const plainText = extractPlainText(element).trim();
      const sentences = splitIntoSentences(plainText);
      newBlockContext = {
        sentences,
        currentSentenceIdx: 0,
        currentProgress: "",
      };
    }

    // Get children
    const children: React.ReactNode[] = [];
    element.childNodes.forEach((child, idx) => {
      const childResult = processNode(child, `${keyPrefix}-${idx}`, context, newBlockContext);
      if (childResult !== null) {
        children.push(childResult);
      }
    });
    
    // After processing a block element, increment global sentence index
    if (isBlockElement && newBlockContext) {
      // Count how many sentences were in this block
      context.globalSentenceIndex += Math.max(1, newBlockContext.sentences.length);
    }

    const props: Record<string, unknown> = { key: keyPrefix || "root" };

    // Map tag names to React elements with appropriate styling
    switch (tagName) {
      case "h1":
        return (
          <h1
            {...props}
            className="text-xl font-semibold mt-6 mb-3 text-foreground first:mt-0"
          >
            {children}
          </h1>
        );
      case "h2":
        return (
          <h2
            {...props}
            className="text-lg font-semibold mt-5 mb-2 text-foreground"
          >
            {children}
          </h2>
        );
      case "h3":
        return (
          <h3
            {...props}
            className="text-base font-semibold mt-4 mb-2 text-foreground"
          >
            {children}
          </h3>
        );
      case "h4":
        return (
          <h4
            {...props}
            className="text-sm font-semibold mt-3 mb-1 text-foreground"
          >
            {children}
          </h4>
        );
      case "p":
        return (
          <p {...props} className="mb-4 last:mb-0">
            {children}
          </p>
        );
      case "strong":
      case "b":
        return <strong {...props}>{children}</strong>;
      case "em":
      case "i":
        return <em {...props}>{children}</em>;
      case "ul":
        return (
          <ul {...props} className="list-disc list-inside mb-4 space-y-1">
            {children}
          </ul>
        );
      case "ol":
        return (
          <ol {...props} className="list-decimal list-inside mb-4 space-y-1">
            {children}
          </ol>
        );
      case "li":
        return <li {...props}>{children}</li>;
      case "a":
        return (
          <a
            {...props}
            href={(element as HTMLAnchorElement).href}
            className="text-primary hover:underline"
            target="_blank"
            rel="noopener noreferrer"
          >
            {children}
          </a>
        );
      case "blockquote":
        return (
          <blockquote
            {...props}
            className="border-l-4 border-primary/30 pl-4 italic my-4"
          >
            {children}
          </blockquote>
        );
      case "code":
        return (
          <code {...props} className="bg-muted px-1 py-0.5 rounded text-sm">
            {children}
          </code>
        );
      case "pre":
        return (
          <pre
            {...props}
            className="bg-muted p-4 rounded-md overflow-x-auto mb-4"
          >
            {children}
          </pre>
        );
      case "hr":
        return <hr {...props} className="my-6 border-border" />;
      case "br":
        return <br {...props} />;
      case "body":
      case "html":
      case "head":
        return <>{children}</>;
      default:
        return React.createElement(tagName, props, children);
    }
  }

  return null;
}

function processTextNode(
  text: string,
  keyPrefix: string,
  context: MatchContext,
  blockContext: BlockContext
): React.ReactNode {
  if (!text || blockContext.sentences.length === 0) {
    return text;
  }

  const elements: React.ReactNode[] = [];
  let remainingText = text;
  let elementIndex = 0;

  while (remainingText.length > 0 && blockContext.currentSentenceIdx < blockContext.sentences.length) {
    const currentSentence = blockContext.sentences[blockContext.currentSentenceIdx];
    const remainingInSentence = currentSentence.slice(
      blockContext.currentProgress.length
    );

    // Handle leading whitespace
    const leadingWs = remainingText.match(/^\s+/);
    if (leadingWs) {
      elements.push(leadingWs[0]);
      remainingText = remainingText.slice(leadingWs[0].length);
      if (blockContext.currentProgress.length === 0) {
        continue;
      }
    }

    if (remainingText.length === 0) break;

    // Character by character matching, ignoring whitespace differences
    let ti = 0; // text index
    let si = 0; // sentence index

    while (ti < remainingText.length && si < remainingInSentence.length) {
      const tc = remainingText[ti];
      const sc = remainingInSentence[si];

      if (/\s/.test(tc) && /\s/.test(sc)) {
        ti++;
        si++;
        continue;
      }
      if (/\s/.test(tc)) {
        ti++;
        continue;
      }
      if (/\s/.test(sc)) {
        si++;
        continue;
      }

      if (tc === sc) {
        ti++;
        si++;
      } else {
        break;
      }
    }

    const textMatchLength = ti;
    const sentenceMatchLength = si;

    if (textMatchLength > 0) {
      const matchedText = remainingText.slice(0, textMatchLength);
      const globalIdx = context.globalSentenceIndex + blockContext.currentSentenceIdx;
      const isHighlighted = context.highlightedSentenceIndex === globalIdx;

      elements.push(
        <span
          key={`${keyPrefix}-${elementIndex++}`}
          onClick={() => context.onSentenceClick(globalIdx)}
          className={`cursor-pointer transition-all duration-200 ${
            isHighlighted
              ? "bg-primary/15 text-foreground"
              : "hover:bg-muted/10"
          }`}
        >
          {matchedText}
        </span>
      );

      remainingText = remainingText.slice(textMatchLength);
      blockContext.currentProgress += remainingInSentence.slice(0, sentenceMatchLength);

      // Check if we've completed the current sentence
      const normalizedProgress = blockContext.currentProgress.replace(/\s+/g, " ").trim();
      const normalizedSentence = currentSentence.replace(/\s+/g, " ").trim();
      
      if (normalizedProgress === normalizedSentence) {
        blockContext.currentSentenceIdx++;
        blockContext.currentProgress = "";
      }
    } else {
      elements.push(remainingText[0]);
      remainingText = remainingText.slice(1);
    }
  }

  if (remainingText.length > 0) {
    elements.push(remainingText);
  }

  return elements.length === 1 ? elements[0] : <>{elements}</>;
}
