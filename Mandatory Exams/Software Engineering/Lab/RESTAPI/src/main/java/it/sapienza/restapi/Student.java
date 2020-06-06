/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package it.sapienza.restapi;

import javax.xml.bind.annotation.XmlRootElement;

@XmlRootElement(name = "Student")
public class Student {
    private int id;
    private String name;

    public int getId() {
        return this.id;
    }
    public String getName(){
        return name;
    }

    public void setId(int i) {
        this.id = i;
    }
    public void setName(String name) {
        this.name = name;
    }
 
}