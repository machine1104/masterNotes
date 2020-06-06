package client;

import client.session.Utente;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Observable;
import java.util.Observer;
import java.util.Properties;

import javax.jms.JMSException;
import javax.jms.Message;
import javax.jms.MessageListener;
import javax.jms.Session;
import javax.jms.TextMessage;
import javax.jms.Topic;
import javax.jms.TopicConnection;
import javax.jms.TopicConnectionFactory;
import javax.jms.TopicPublisher;
import javax.jms.TopicSession;
import javax.jms.TopicSubscriber;
import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;

public class CompraJMSManager extends Observable implements MessageListener {
	
        Properties properties = null;
        Context jndiContext = null;
	private TopicConnectionFactory connectionFactory = null;
	private TopicConnection connection = null;
	private TopicSession session = null;
	private Topic destination = null;
	private TopicSubscriber sub;
        private TopicPublisher topicPublisher;
        

	public CompraJMSManager(Observer osservatore) {
		super.addObserver(osservatore);

		try {
			
                    InitialContext ctx = null;
                    properties = new Properties();
		    properties.setProperty(Context.INITIAL_CONTEXT_FACTORY,"org.apache.activemq.jndi.ActiveMQInitialContextFactory");
                    properties.setProperty(Context.PROVIDER_URL,"tcp://localhost:61616");
                    jndiContext = new InitialContext(properties);        
                
                    ctx = new InitialContext(properties);
		    this.connectionFactory =
			(TopicConnectionFactory) ctx.lookup("ConnectionFactory");
		    this.destination =
			(Topic) ctx.lookup("dynamicTopics/Ordini");

		    this.connection =
			this.connectionFactory.createTopicConnection();
		    this.session =
			this.connection.createTopicSession(
					false, Session.AUTO_ACKNOWLEDGE
				);
                 this.topicPublisher = session.createPublisher(destination);
		} catch (NamingException err) {
			err.printStackTrace();
		} catch (JMSException err) {
			err.printStackTrace();
		} 
	}
	
	public boolean compra(String nome, float prezzo, int quantita) {
		String utente = Utente.getInstance().getUtente();
		
		if (utente == null)
			return false;
		
		try {
			TextMessage sendMex = session.createTextMessage();
			
			sendMex.setStringProperty("Utente",
					utente
				);
			sendMex.setStringProperty("Nome",
					nome
				);
			sendMex.setFloatProperty("Prezzo",
					prezzo
				);

			sendMex.setIntProperty("Quantita", quantita);
			String query =
					"Utente = '" + utente + "'" +
					" AND " +
					"Nome = '" + nome + "'";
			sub = session.createSubscriber(destination, query, true);
			sub.setMessageListener(this);
			connection.start();
			topicPublisher.publish(sendMex);
		} catch (JMSException err) {
			err.printStackTrace();
			return false;
		}
		return true;
	}

	/**
	 * Invocato quando la notifica positiva o negativa dell'acquisto giunge a
	 * destinazione
	 * 
	 * @param mex
	 *            Il messaggio di notifica.
	 */
	public void onMessage(Message mex) {
		String infoMex = null;
		try {
			TextMessage recMex = (TextMessage) mex;
			
			if (recMex != null)
				if (recMex.getBooleanProperty("Status"))
					infoMex = "L'acquisto \u00e8 andato a buon fine";
				else
					infoMex = "L'acquisto non \u00e8 andato a buon fine";
			/*
			 * Chiude la connessione del subscriber asincrono in modo da non
			 * ricevere altri messaggi di notifica
			 */
			sub.close();
		} catch (NumberFormatException err) {
			infoMex = "Errore nel riempimento di alcuni campi";
		} catch (JMSException err) {
			err.printStackTrace();
		}
		
		if (infoMex != null) {
			super.setChanged();	// rende attivo il cambiamento di stato
			super.notifyObservers(infoMex);
		}
	}

}