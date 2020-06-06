/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package exrmicl;

import svriface.ServerInterface;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.Arrays;

import svriface.*;

/**
 *
 * @author biar
 */
public class ExRMICl {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws Exception {
        Registry registry = LocateRegistry.getRegistry("localhost", 5555);
        ServerInterface stub = (ServerInterface) registry.lookup("Server");
        int myID = stub.startTask();
        Thread.sleep(4500);
        while ( stub.isReady(myID) ) 
        {
            System.out.println("... sto aspettando ...");
            Thread.sleep(4500);
        }
        System.out.println(Arrays.toString(stub.getResults(myID)));
    }
    
}
