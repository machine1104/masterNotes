package client;

import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) throws IOException, InterruptedException {
        Socket sock = new Socket(args[0], Integer.parseInt(args[1]));
        OutputStream os = sock.getOutputStream();
        PrintWriter netPw = new PrintWriter(new OutputStreamWriter(os));
        Scanner scan = new Scanner(sock.getInputStream());

        System.out.println(".. sto per mandare start ...");
        netPw.println("start");
        netPw.flush();
        Thread.sleep(3000);
        
        
        boolean finished = false;
        while (!finished) {
            System.out.println(".. sto per chiedere getStatus ...");
            netPw.println("getStatus");
            netPw.flush();
            String cmd = scan.nextLine();
            System.out.println(".. ho ricevuto " + cmd);
            if (cmd.equals("finished")) {
                finished = true;
            }
            Thread.sleep(3000);
        }

        ArrayList resultBuffer = new ArrayList();
        System.out.println(".. sto per chiedere getResult ...");
        netPw.println("getResult");
        netPw.flush();
        boolean goon = true;
        while (goon) {
            String cmd = scan.nextLine();
            if (cmd.equals("###")) {
                goon = false;
            } else {
                resultBuffer.add(Integer.parseInt(cmd));
            }
        }
        
        System.out.println(resultBuffer);
        
    }

}