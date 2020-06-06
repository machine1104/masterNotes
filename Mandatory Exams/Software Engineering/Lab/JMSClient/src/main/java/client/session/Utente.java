package client.session;

/*
 * CLASSE SINGLETON (NE ESISTE SEMPRE UNA SOLA INSTANZA!)
 */
public class Utente {
	private static Utente istanza = new Utente();
	private String utente = null;
	
	private Utente() {}
	
	public static final Utente getInstance() {
		return istanza;
	}

	public String getUtente() {
		return (utente);
	}

	public void setUtente(String utente) {
		this.utente = utente;
	}
}