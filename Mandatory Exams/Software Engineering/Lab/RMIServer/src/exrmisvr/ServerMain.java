/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package exrmisvr;

import svriface.ServerInterface;
import java.rmi.registry.*;
import java.rmi.server.*;

public class ServerMain {

    public static void main(String[] args) {
        try {
            ServerImpl obj = new ServerImpl();
            ServerInterface stub = (ServerInterface) UnicastRemoteObject.exportObject(obj, 0);

            // Bind the remote object's stub in the registry
            Registry registry = LocateRegistry.createRegistry(5555);
            registry.rebind("Server", stub);

            System.out.println("Server ready");
        } catch (Exception e) {
            System.err.println("Server exception: " + e.toString());
            e.printStackTrace();
        }
    }
}
