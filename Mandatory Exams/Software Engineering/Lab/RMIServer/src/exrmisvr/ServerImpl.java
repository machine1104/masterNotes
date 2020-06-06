/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package exrmisvr;

import svriface.ServerInterface;
import java.rmi.*;
import java.util.*;

public class ServerImpl implements ServerInterface {

    Hashtable<Integer, ServerThread> threadPool;
    int allocatedThreads;
    
    public ServerImpl() {
        this.threadPool = new Hashtable<Integer,ServerThread>();
        this.allocatedThreads = 0;
    }

    @Override
    public int startTask() throws RemoteException {
        System.out.println("RMI Server" + Thread.currentThread() + "e' stato richiesto startTask() ...");
        
        ServerThread st = new ServerThread();
        Thread t = new Thread(st);
        threadPool.put(allocatedThreads, st);
        t.start();
        allocatedThreads = allocatedThreads + 1;
        return (allocatedThreads-1);
    }

    public boolean isReady(int i) throws RemoteException {
        //System.out.println("RMI Server" + Thread.currentThread() + "e' stato richiesto isReady() ...");
        return threadPool.get(i).isRunning();
    }

    public int[] getResults(int i) throws RemoteException {
        System.out.println("RMI Server" + Thread.currentThread() + "e' stato richiesto getResults() ...");
        return threadPool.get(i).getResult();
    }
}
