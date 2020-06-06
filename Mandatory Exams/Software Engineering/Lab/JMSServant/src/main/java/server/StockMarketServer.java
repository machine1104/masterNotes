package server;

import java.net.InetSocketAddress;
import java.net.Socket;

public class StockMarketServer {

	public static void main(String args[]) throws Exception {
            
        boolean serverReady = false;
        
        while(!serverReady){
            Socket socket = new Socket();
            try{
                socket.connect(new InetSocketAddress("broker", 8161),5000);
                socket.close();
                serverReady = true;
                System.out.println("....broker finally ready!");
                
            }catch(Exception e){
                serverReady = false;
                System.out.println(".....broker not ready!");
            }
        }
            
	NotificatoreAcquisto n = new NotificatoreAcquisto();
        n.start();	
            
        ProduttoreQuotazioni q = new ProduttoreQuotazioni();
        q.start();
                
                
	}
}