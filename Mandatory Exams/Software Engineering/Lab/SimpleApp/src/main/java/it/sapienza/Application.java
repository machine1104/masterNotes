/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package it.sapienza;

import java.util.Properties;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.jms.BytesMessage;
import javax.naming.Context;
import javax.jms.Connection;
import javax.jms.ConnectionFactory;
import javax.jms.Destination;
import javax.jms.JMSException;
import javax.jms.Message;
import javax.jms.MessageConsumer;
import javax.jms.Session;
import javax.jms.TextMessage;
import javax.jms.Topic;
import javax.naming.InitialContext;
import javax.naming.NamingException;

/**
 *
 * @author studente
 */
public class Application {

    private Context jndiContext = null;
    private ConnectionFactory connectionFactory = null;        
    private Connection connection = null;
    private Session session = null;
    private Destination destination = null;
    private String destinationName = "dynamicTopics/Quotazioni";
    private MessageConsumer messageConsumer = null;
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Application application = new Application();
        application.createConnection();
        application.getMessages();
    }
    
    private void createConnection(){
        Properties props = new Properties();
        props.setProperty(Context.INITIAL_CONTEXT_FACTORY,"org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        props.setProperty(Context.PROVIDER_URL,"tcp://127.0.0.1:61616"); 
        try{
            jndiContext = new InitialContext(props);
            System.out.println("+--:"+jndiContext);
            connectionFactory = (ConnectionFactory)jndiContext.lookup("ConnectionFactory"); 
            System.out.println("+--:"+connectionFactory);
            destination = (Destination)jndiContext.lookup(destinationName);
            System.out.println("+--:"+destination);
            connection = connectionFactory.createConnection();
            System.out.println("+--:"+connection);
            session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
            System.out.println("+--:"+session);
            messageConsumer = session.createConsumer(destination);
            System.out.println("+--:"+messageConsumer);
            connection.start();
        } catch (NamingException nex){
            nex.printStackTrace();
        }
        catch (JMSException ex) {
            ex.printStackTrace();
        }
    }
    
    private void getMessages(){  
        try{
            Message message;
            while(true){
                message = messageConsumer.receive();
                String text="";
                if (message instanceof TextMessage)
                {
                    text = ((TextMessage) message).getText();
                }
                System.out.println("Received  message:  " + text);
            }
        } catch(Exception ex){
            ex.printStackTrace();
        }
    }
}
