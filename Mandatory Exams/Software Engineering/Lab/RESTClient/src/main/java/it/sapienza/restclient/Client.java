/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package it.sapienza.restclient;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;

import javax.xml.bind.JAXB;

import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpDelete;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.entity.InputStreamEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;

public class Client {

    private static final String BASE_URL = "http://localhost:8080/courses/";
    private static CloseableHttpClient client;

    public static void main(String[] args) throws IOException{
    client = HttpClients.createDefault();
    
    // Example GET
    Course course = getCourse(1);
    System.out.println(course);
    for (int i = 0; i < course.getStudents().size(); i++) {
        Student student = course.getStudents().get(i);
        System.out.println(student);
    }
    
    // Example POST/PUT
    course = getCourse(2);
    System.out.println(course);
    for (int i = 0; i < course.getStudents().size(); i++) {
        Student student = course.getStudents().get(i);
        System.out.println(student);
    }
    createValidStudent();
    course = getCourse(2);
    System.out.println(course);
    for (int i = 0; i < course.getStudents().size(); i++) {
        Student student = course.getStudents().get(i);
        System.out.println(student);
    }
    
    
    client.close();
    
        
    }

      private static Student getStudent(int courseOrder, int studentOrder) throws IOException {
        final URL url = new URL(BASE_URL + courseOrder + "/students/" + studentOrder);
        final InputStream input = url.openStream();
        return JAXB.unmarshal(new InputStreamReader(input), Student.class);
    }

      private static Course getCourse(int courseOrder) throws IOException {
        final URL url = new URL(BASE_URL + courseOrder);
        final InputStream input = url.openStream();
        return JAXB.unmarshal(new InputStreamReader(input), Course.class);
    }

      
      
    private static void createValidStudent() throws IOException {
        final HttpPost httpPost = new HttpPost(BASE_URL + "2/students");
        final InputStream resourceStream =  Client.class.getClassLoader().getResourceAsStream("newStudent.xml");
        httpPost.setEntity(new InputStreamEntity(resourceStream));
        httpPost.setHeader("Content-Type", "text/xml");

        final HttpResponse response = client.execute(httpPost);
        
    }
    

}  