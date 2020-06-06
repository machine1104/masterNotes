package soapwebserviceclient;

import it.sapienza.soapwebservice.Student;
import it.sapienza.soapwebservice.StudentEntry;
import it.sapienza.soapwebservice.StudentMap;
import java.util.List;

/**
 *
 * @author studente
 */
public class Application {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Application application = new Application();
        application.init();
    }

    private void init(){

        /*Student s2 = new Student();
        s2.setName("Giovanni");
        String result1 = helloStudent(s1);
        System.out.println(result1);
        String result2 = helloStudent(s2);
        System.out.println(result2);
        */
        StudentMap map = getStudents();

        List<StudentEntry> list = map.getEntry();
        System.out.print("Got " + list.size() + " students");
        for(StudentEntry entry : list){
            Integer id = entry.getId();
            Student student = entry.getStudent();
            System.out.println("Student with name: " + student.getName());
        }
        Student s1 = new Student();
        s1.setName("Stefano");
        //String result1 = 
        helloStudent(s1);

        map = getStudents();
        list = map.getEntry();
        System.out.print("Got " + list.size() + " students");
        for(StudentEntry entry : list){
            Integer id = entry.getId();
            Student student = entry.getStudent();
            System.out.println("Student with name: " + student.getName());
        }
    }

    private static StudentMap getStudents() {
        it.sapienza.soapwebservice.WSImplService service = new it.sapienza.soapwebservice.WSImplService();
        it.sapienza.soapwebservice.WSInterface port = service.getWSImplPort();
        return port.getStudents();
    }

    private static String hello(java.lang.String arg0) {
        it.sapienza.soapwebservice.WSImplService service = new it.sapienza.soapwebservice.WSImplService();
        it.sapienza.soapwebservice.WSInterface port = service.getWSImplPort();
        return port.hello(arg0);
    }

    private static String helloStudent(it.sapienza.soapwebservice.Student arg0) {
        it.sapienza.soapwebservice.WSImplService service = new it.sapienza.soapwebservice.WSImplService();
        it.sapienza.soapwebservice.WSInterface port = service.getWSImplPort();
        return port.helloStudent(arg0);
    }
    
}
