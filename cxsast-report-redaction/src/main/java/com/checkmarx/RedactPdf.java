package com.checkmarx;

import org.apache.pdfbox.pdmodel.*;
import org.apache.pdfbox.pdmodel.common.PDRectangle;
import org.apache.pdfbox.pdmodel.font.PDType1Font;
import org.apache.pdfbox.contentstream.PDFStreamEngine;

import java.awt.*;
import java.io.File;
import java.io.IOException;

import static java.lang.System.exit;

/**
 * Creates a new, redacted, PDF, containing only the first page
 * of the original and a note that the rest has been intentionally
 * removed.
 */
public class RedactPdf extends PDFStreamEngine {

    public RedactPdf() {

    }

    /**
     * @param args The command line arguments.
     * @throws IOException If there is an error parsing the document.
     */
    public static void main(String[] args) throws IOException {

        if (args.length != 1 && args.length != 2) {
            System.out.println("Unsupported number of arguments, expected 1 or 2 args but got " + args.length);
            System.out.println("The command line arguments were: ");
            for (int x = 0; x< args.length; x++) {
                System.out.println("args[" + x + "]: " + args[x]);
            }
            Usage();
            exit(1);
        }

        String originalPdf =  args[0];
        String redactedFilename = "redacted-report.pdf";
        if (args.length == 2) {
            redactedFilename = args[1]; // override the new file name
        }

        File inputFile = new File(originalPdf);
        if (!inputFile.exists()) {
            System.out.println("The input file at " + originalPdf + " does not exist");
            exit(2);
        }

        File outputFile = new File(redactedFilename);
        if (outputFile.exists()) {
            System.out.println("The output file at " + redactedFilename + " already exists and will be overwritten");
        }
        try {
            outputFile.createNewFile();
        } catch (Exception ex) {
            System.out.println("Cannot create file at the destination: " + redactedFilename);
            exit(3);
        }

        CreateRedactedPDF(originalPdf, redactedFilename);
        System.out.println("Created redacted PDF at " + redactedFilename);
    }

    public static void Usage() {

        System.out.println();
        System.out.println("com.checkmarx.RedactPdf.jar - used to remove everything but the cover page from Checkmarx CxSAST PDF reports");
        System.out.println();
        System.out.println("Arguments, by position:");
        System.out.println("[0] REQUIRED the path to the pdf file that you want to redact");
        System.out.println("[1] OPTIONAL the filename of the redacted report. Default is redacted-report.pdf. Rename your report in your calling environment with additional metadata available there");
        System.out.println();
        System.out.println("Usage: ");
        System.out.println();
        System.out.println("java -jar com.checkmarx.RedactPdf.jar \"/path/to/original_report.pdf\"");
        System.out.println();
        System.out.println("java -jar com.checkmarx.RedactPdf.jar \"/path/to/original_report.pdf\" \"the-new-filename.pdf\"");
        System.out.println();
        System.out.println("Notes: ");
        System.out.println(" * The caller is responsible for deleting the original PDF file if that is required");
        System.out.println();

    }

    public static void CreateRedactedPDF(String originalFilename, String redactedFilename) throws IOException {

        PDDocument document = null;
        PDDocument redactedPdf = null;

        try {
            // Load the existing PDF
            File file = new File(originalFilename);
            document = PDDocument.load(file);

            // Create a new PDF, with just the first page of the original
            PDPage firstPage = document.getPage(0);
            redactedPdf = new PDDocument();
            redactedPdf.addPage(firstPage);

            // Add a second page, for our note
            PDPage secondPage = new PDPage(PDRectangle.A4);
            redactedPdf.addPage(secondPage);

            // Add the note
            PDPageContentStream cs = new PDPageContentStream(redactedPdf, secondPage);
            cs.beginText();
            cs.setFont(PDType1Font.TIMES_ROMAN, 14);
            cs.setNonStrokingColor(Color.black);
            cs.newLineAtOffset(125, 775);
            cs.showText("The remainder of this report has been intentionally removed.");
            cs.newLine();
            cs.endText();
            cs.close();

            // Save the file
            redactedPdf.save(redactedFilename);

        } finally {
            if (document != null) {
                document.close();
            }
            if (redactedPdf != null) {
                redactedPdf.close();
            }
        }
    }
}