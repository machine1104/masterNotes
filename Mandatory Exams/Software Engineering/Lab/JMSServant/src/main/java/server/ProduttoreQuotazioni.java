package server;

import javax.jms.*;
import javax.naming.*;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Properties;
import java.util.Random;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ProduttoreQuotazioni {
	final String titoli[] = { "Telecom", "Finmeccanica", "Banca_Intesa",
			"Oracle", "Parmalat", "Mondadori", "Vodafone", "Barilla" };

	private String scegliTitolo() {
		int whichMsg;
		Random randomGen = new Random();

		whichMsg = randomGen.nextInt(this.titoli.length);
		return this.titoli[whichMsg];
	}

	private float valore() {
		Random randomGen = new Random();
		float val = randomGen.nextFloat() * this.titoli.length * 10;
		return val;
	}

        private static final Logger LOG = LoggerFactory.getLogger(ProduttoreQuotazioni.class);
        
	public void start() throws NamingException, JMSException {
                
                Context jndiContext = null;
                ConnectionFactory connectionFactory = null;
                Connection connection = null;
                Session session = null;
                Destination destination = null;
                MessageProducer producer = null;
                String destinationName = "dynamicTopics/Quotazioni";
        
                /*
         * Create a JNDI API InitialContext object
         */
        
        try {
            
            Properties props = new Properties();
        
props.setProperty(Context.INITIAL_CONTEXT_FACTORY,"org.apache.activemq.jndi.ActiveMQInitialContextFactory");
//props.setProperty(Context.PROVIDER_URL,"tcp://localhost:61616");
props.setProperty(Context.PROVIDER_URL,"tcp://broker:61616");
jndiContext = new InitialContext(props);        
                
        } catch (NamingException e) {
            LOG.info("ERROR in JNDI: " + e.toString());
            System.exit(1);
        }

        /*
         * Look up connection factory and destination.
         */
        try {
            connectionFactory = (ConnectionFactory)jndiContext.lookup("ConnectionFactory");
            destination = (Destination)jndiContext.lookup(destinationName);
        } catch (NamingException e) {
            LOG.info("JNDI API lookup failed: " + e);
            System.exit(1);
        }

        /*
         * Create connection. Create session from connection; false means
         * session is not transacted. Create sender and text message. Send
         * messages, varying text slightly. Send end-of-messages message.
         * Finally, close connection.
         */
        try {
            connection = connectionFactory.createConnection();
            session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
            producer = session.createProducer(destination);
            
              
                
                TextMessage message = null;
		String messageType = null;
		
                message = session.createTextMessage();

                float quotazione;
		int i = 0;
		while (true) {
			i++;
			messageType = scegliTitolo();
			quotazione = valore();
			message.setStringProperty("Nome", messageType);
			message.setFloatProperty("Valore", quotazione);
			message.setText(
					"Item " + i + ": " + messageType + ", Valore: "
					+ quotazione);

			    LOG.info(
					this.getClass().getName() + 
				        "Invio quotazione: " + message.getText());

			producer.send(message);

			try {
				Thread.sleep(5000);
			} catch (Exception ex) {
				ex.printStackTrace();
			}
		}
	}
        
        catch (JMSException e) {
            LOG.info("Exception occurred: " + e);
        } finally {
            if (connection != null) {
                try {
                    connection.close();
                } catch (JMSException e) {
                }
            }
        }
}
}