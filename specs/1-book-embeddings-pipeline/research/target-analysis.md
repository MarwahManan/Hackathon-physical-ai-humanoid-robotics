# Target Website Analysis: Physical AI & Humanoid Robotics

**Feature**: 1-book-embeddings-pipeline
**Created**: 2025-12-20
**Status**: Completed

## Website Overview

### Target URL
- **Base**: https://physical-ai-humanoid-robotics-vert.vercel.app/
- **Content Type**: Educational resource on Physical AI & Humanoid Robotics
- **Structure**: Docusaurus-based documentation site

### Content Inventory
- 4 main chapters with multiple lessons each
- Specialized modules (ROS 2, Digital Twin, AI Robot Brain, VLA)
- Research articles and papers
- Blog posts with technical insights
- Introduction and getting started guides

### URL Patterns Identified
1. `/docs/intro` - Main introduction
2. `/docs/physical-ai-humanoid-robotics/chapter-X/lesson-X-X-*` - Core curriculum
3. `/docs/modules/*` - Specialized technology modules
4. `/docs/research-articles` - Research content
5. `/blog/*` - Blog posts and articles

## Technical Architecture

### Page Structure
- Standard Docusaurus layout with navigation
- Content in `<main>` or `.markdown` elements
- Minimal dynamic content (mostly static)
- Well-structured HTML with semantic elements

### Text Extraction Strategy
- Target main content containers: `main`, `.markdown`, `.theme-doc-markdown`
- Exclude navigation, headers, footers, and sidebar elements
- Extract headings, paragraphs, lists, and code blocks
- Preserve document hierarchy in metadata

## Crawling Approach

### Discovery Method
- Start with sitemap if available
- Follow internal navigation links
- Respect robots.txt directives
- Implement breadth-first traversal to cover all content

### Rate Limiting
- Conservative approach: 1 request per second
- Respect server response headers (Retry-After, etc.)
- Handle 429 responses with exponential backoff
- Monitor for performance impact on target server

## Content Characteristics

### Text Density
- High-quality educational content
- Technical terminology and concepts
- Structured with headings and subheadings
- Code examples and implementation details

### Content Length
- Individual pages: 500-3000 words average
- Need to chunk appropriately for embedding models
- Preserve semantic coherence within chunks