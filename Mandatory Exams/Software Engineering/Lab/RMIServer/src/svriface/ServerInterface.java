/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package svriface;

import java.rmi.Remote;
import java.rmi.RemoteException;

public interface ServerInterface extends Remote {

   int startTask() throws RemoteException;
   boolean isReady(int id) throws RemoteException;
   int[] getResults(int id) throws RemoteException;
}
