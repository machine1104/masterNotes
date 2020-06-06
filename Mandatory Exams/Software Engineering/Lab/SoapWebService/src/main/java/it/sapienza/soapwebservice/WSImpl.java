package it.sapienza.soapwebservice;

import java.util.LinkedHashMap;
import java.util.Map;
import javax.jws.WebService;

/**
 *
 * @author studente
 */
@WebService(endpointInterface = "it.sapienza.soapwebservice.WSInterface")
public class WSImpl implements WSInterface {
    private Map<Integer, Student> students 
      = new LinkedHashMap<Integer, Student>();
 
    public String hello(String name) {
        return "Hello " + name;
    }
 
    public String helloStudent(Student student) {
        students.put(students.size() + 1, student);
        return "Hello " + student.getName();
    }
 
    public Map<Integer, Student> getStudents() {
        return students;
    }
}