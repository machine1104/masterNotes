package client.gui;

import client.session.Utente;

import javax.swing.*;
import java.awt.*;
import java.util.Observable;
import java.util.Observer;

public class CompraFrame extends JFrame implements Observer {
	/** Larghezza dei campi per le etichette */
	private static final int LABEL_WIDTH = 120;

	// etichette
	private JLabel utenteLbl = new JLabel("Utente:");
	private JLabel nomeLbl = new JLabel("Nome:");
	private JLabel prezzoLbl = new JLabel("Prezzo:");
	private JLabel quantitaLbl = new JLabel("Quantit\u00e0:");
	private JLabel importoComplessivoLbl = new JLabel("Importo:");
	private JLabel euroPrezzoLbl = new JLabel("\u20ac");
	private JLabel euroImportoLbl = new JLabel("\u20ac");

	// etichette aggiornabili
	private JLabel utenteTxtLbl = new JLabel();
	private JLabel importoComplessivoValoreLbl = new JLabel("0.00");

	// pannelli
	private JPanel utentePnl = new JPanel(new FlowLayout(FlowLayout.LEFT));
	private JPanel nomePnl = new JPanel(new FlowLayout(FlowLayout.LEFT));
	private JPanel prezzoPnl = new JPanel(new FlowLayout(FlowLayout.LEFT));
	private JPanel quantitaPnl = new JPanel(new FlowLayout(FlowLayout.LEFT));
	private JPanel importoComplessivoPnl = new JPanel(new FlowLayout(FlowLayout.LEFT));

	private JPanel centroPnl = new JPanel();
	private JPanel sudPnl = new JPanel();

	// widget di input
	private JTextField nomeTxt = new JTextField(20);
	private JTextField prezzoTxt = new JTextField(10);
	private JTextField quantitaTxt = new JTextField(5);

	// pulsanti
	private JButton ordinaBtn = new JButton("Ordina");

	// ascoltatori
	private CompraListener ascoltatore = new CompraListener(this);

	public CompraFrame() {
		super("Effettua Acquisti");

		this.utenteTxtLbl.setText(Utente.getInstance().getUtente());
		
		this.impostaCaratteristicheGraficheEtichette();

		// aggiunge i widget ai pannelli
		this.utentePnl.add(utenteLbl);
		this.utentePnl.add(utenteTxtLbl);
		this.nomePnl.add(nomeLbl);
		this.nomePnl.add(nomeTxt);
		this.prezzoPnl.add(prezzoLbl);
		this.prezzoPnl.add(prezzoTxt);
		this.prezzoPnl.add(euroPrezzoLbl);
		this.quantitaPnl.add(quantitaLbl);
		this.quantitaPnl.add(quantitaTxt);

		this.prezzoTxt.addFocusListener(ascoltatore);
		this.quantitaTxt.addFocusListener(ascoltatore);
		this.ordinaBtn.addActionListener(ascoltatore);

		this.importoComplessivoPnl.add(importoComplessivoLbl);
		this.importoComplessivoPnl.add(importoComplessivoValoreLbl);
		this.importoComplessivoPnl.add(euroImportoLbl);

		this.centroPnl.setLayout(new BoxLayout(centroPnl, BoxLayout.Y_AXIS));
		
		this.centroPnl.add(utentePnl);
		this.centroPnl.add(nomePnl);
		this.centroPnl.add(prezzoPnl);
		this.centroPnl.add(quantitaPnl);
		this.centroPnl.add(importoComplessivoPnl);

		this.sudPnl.add(ordinaBtn);

		this.getContentPane().add(centroPnl, BorderLayout.CENTER);
		this.getContentPane().add(sudPnl, BorderLayout.SOUTH);

		this.pack();
	}

	private void impostaCaratteristicheGraficheEtichette() {
		// usato solo in quanto la dimensione di default per le etichette prevede
		// l'inserimento sia della larghezza, che ci interessa, sia dell'altezza
		int labelHeight = this.utenteLbl.getPreferredSize().height;

		this.utenteLbl
				.setPreferredSize(new Dimension(LABEL_WIDTH, labelHeight));
		this.nomeLbl
				.setPreferredSize(new Dimension(LABEL_WIDTH, labelHeight));
		this.prezzoLbl
				.setPreferredSize(new Dimension(LABEL_WIDTH, labelHeight));
		this.quantitaLbl
				.setPreferredSize(new Dimension(LABEL_WIDTH, labelHeight));
		this.importoComplessivoLbl
				.setPreferredSize(new Dimension(LABEL_WIDTH, labelHeight));
		
		this.utenteLbl
				.setHorizontalAlignment(JLabel.RIGHT);
		this.nomeLbl
				.setHorizontalAlignment(JLabel.RIGHT);
		this.prezzoLbl
				.setHorizontalAlignment(JLabel.RIGHT);
		this.quantitaLbl
				.setHorizontalAlignment(JLabel.RIGHT);
		this.importoComplessivoLbl
				.setHorizontalAlignment(JLabel.RIGHT);
	}
	
	public void notificaErrore(String errore) {
		JOptionPane.showMessageDialog(
				this,
				errore,
				this.getTitle(),
				JOptionPane.ERROR_MESSAGE);
	}
	
	// Metodi di accesso ai campi

	public String getQuantita() {
		return this.quantitaTxt.getText();
	}

	public String getPrezzo() {
		return this.prezzoTxt.getText();
	}
	
	public String getNome() {
		return this.nomeTxt.getText();
	}

	public void setNome(String nome) {
		this.nomeTxt.setText(nome);
	}

	public void impostaImportoComplessivo(String importoComplessivo) {
		this.importoComplessivoValoreLbl.setText(importoComplessivo);
	}

	@Override
	public void update(Observable o, Object arg) {
		JOptionPane.showMessageDialog(
				this,
				arg.toString(),
				this.getTitle(),
				JOptionPane.INFORMATION_MESSAGE);
	}
}