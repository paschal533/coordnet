import * as pdfjsLib from "pdfjs-dist";
import {
  PDFDocumentProxy,
  PDFPageProxy,
  TextContent,
  TextItem,
  TextMarkedContent,
} from "pdfjs-dist/types/src/display/api";

pdfjsLib.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.mjs`;

/**
 * Reads a PDF file from an ArrayBuffer and extracts its text content as an HTML formatted string.
 * @param {ArrayBuffer} arrayBuffer The ArrayBuffer containing PDF data.
 * @returns {Promise<string>} A promise that resolves to an HTML string with the extracted text content.
 */
export const readPdf = async (arrayBuffer: ArrayBuffer): Promise<string> => {
  const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
  try {
    const pdfDocument: PDFDocumentProxy = await loadingTask.promise;
    let htmlContent: string = "<div>"; // Start with an HTML div container

    // Extract text from each page
    for (let pageNum = 1; pageNum <= pdfDocument.numPages; pageNum++) {
      const page: PDFPageProxy = await pdfDocument.getPage(pageNum);
      const text: TextContent = await page.getTextContent();

      let lastY: number | null = null;
      text.items.forEach((item: TextItem | TextMarkedContent, index: number) => {
        if (lastY !== null && "transform" in item && Math.abs(lastY - item.transform[5]) > 1) {
          htmlContent += "<br>";
        }
        if ("str" in item) {
          htmlContent += item.str;
        }
        lastY = "transform" in item ? item.transform[5] : lastY;

        if (text.items[index + 1] && "transform" in item && "transform" in text.items[index + 1]) {
          if (Math.abs((text.items[index + 1] as TextItem).transform[5] - item.transform[5]) <= 1)
            htmlContent += " ";
        }
      });

      htmlContent += "<br><br>";
    }

    htmlContent += "</div>";
    return htmlContent;
  } catch (error) {
    console.error("Error processing PDF: ", error);
    throw error;
  }
};

export { pdfjsLib };