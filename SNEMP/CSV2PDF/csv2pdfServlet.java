import java.io.*;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
//used to read user uploaded CSV file.
import au.com.bytecode.opencsv.CSVReader; 
//read uploaded file
import org.apache.commons.io.FilenameUtils; 
import java.io.InputStreamReader;
import java.util.*;
import org.apache.commons.fileupload.servlet.ServletFileUpload; 
import org.apache.commons.fileupload.disk.DiskFileItemFactory;
import org.apache.commons.fileupload.*;
//itext libraries to create PDF table 
import com.itextpdf.text.Phrase;
import com.itextpdf.text.Document;
import com.itextpdf.text.pdf.*;


public class csv2pdfServlet extends HttpServlet {
public csv2pdfServlet() {
}
public void doGet(HttpServletRequest request, HttpServletResponse response)
throws ServletException, IOException {
        OutputStream out = response.getOutputStream();  
        
        try {
                InputStream filecontent=null; //Initialize the input stream that accepts the user uploaded CSV file             
                List<FileItem> items = new ServletFileUpload(new DiskFileItemFactory()).parseRequest(request);          
                for (FileItem item : items) {
                        if (item.isFormField()) {                               
                                String fieldname = item.getFieldName();
                                //not applicable in this example, we don't 
                                //have any form fields
                                
                        } else {
                        //The uploaded file is processed in this section
                        String fieldname = item.getFieldName();
                        String filename = FilenameUtils.getName(item.getName());
                        filecontent = item.getInputStream();
                        //Uploaded file is obtained into Inputstream object at this step                
                        }
                }
         // We know the output type and have the file in the input stream now. We can now convert CSV to XLSX and return response back to server

         CSVReader reader = new CSVReader(new InputStreamReader(filecontent)); //reads the input CSV file in the servlet
         String [] nextLine;
         int lnNum = 0;
         
         Document my_pdf_data = new Document();
         PdfWriter.getInstance(my_pdf_data, out);
         my_pdf_data.open();
         //Assuming CSV file will have two column data
         //Expand this if you need more
         PdfPTable my_first_table = new PdfPTable(2);
         PdfPCell table_cell;
        
         while ((nextLine = reader.readNext()) != null) {
                        lnNum++;        
                        table_cell=new PdfPCell(new Phrase(nextLine[0]));
                        my_first_table.addCell(table_cell);
                        table_cell=new PdfPCell(new Phrase(nextLine[1]));
                        my_first_table.addCell(table_cell);                                             
        }
        response.setContentType("application/pdf");
        my_pdf_data.add(my_first_table);                       
        my_pdf_data.close();
       
        
        }
        catch (Exception e) {
               System.err.println(e.toString()); 
         }
         finally {
                 out.close();
         }
        
}
public void doPost(HttpServletRequest request,HttpServletResponse response)
throws ServletException, IOException {
        doGet(request, response);
         }
}
