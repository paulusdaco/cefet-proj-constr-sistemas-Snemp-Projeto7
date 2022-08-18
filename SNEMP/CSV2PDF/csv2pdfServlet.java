import java.io.*;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
//usado para ler o arquivo CSV carregado pelo usuário.
import au.com.bytecode.opencsv.CSVReader; 
//leitura do arquivo enviado
import org.apache.commons.io.FilenameUtils; 
import java.io.InputStreamReader;
import java.util.*;
import org.apache.commons.fileupload.servlet.ServletFileUpload; 
import org.apache.commons.fileupload.disk.DiskFileItemFactory;
import org.apache.commons.fileupload.*;
//bibliotecas do itext para criar tabela PDF
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
                InputStream filecontent=null; //Inicialize o fluxo de entrada que aceita o arquivo CSV carregado pelo usuário             
                List<FileItem> items = new ServletFileUpload(new DiskFileItemFactory()).parseRequest(request);          
                for (FileItem item : items) {
                        if (item.isFormField()) {                               
                                String fieldname = item.getFieldName();
                        } else {
                        //O arquivo enviado é processado nesta seção
                        String fieldname = item.getFieldName();
                        String filename = FilenameUtils.getName(item.getName());
                        filecontent = item.getInputStream();
                        //O arquivo carregado é obtido no objeto Inputstream nesta etapa              
                        }
                }
       

         CSVReader reader = new CSVReader(new InputStreamReader(filecontent)); //lê o arquivo CSV de entrada no servlet
         String [] nextLine;
         int lnNum = 0;
         
         Document my_pdf_data = new Document();
         PdfWriter.getInstance(my_pdf_data, out);
         my_pdf_data.open();
         //Assumindo que o arquivo CSV terá dados de duas colunas
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
