/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package it.sapienza.soapwebservice;

import javax.xml.ws.Endpoint;

public class Server {
    public static void main(String args[]) throws InterruptedException {
        WSInterface implementor = new WSImpl();
        String address = "http://0.0.0.0:7777/WSInterface";
        //String address = "http://localhost:8081/WSInterface";
        Endpoint.publish(address, implementor);
        Thread.sleep(Long.MAX_VALUE);        
        System.exit(0);
    }
}