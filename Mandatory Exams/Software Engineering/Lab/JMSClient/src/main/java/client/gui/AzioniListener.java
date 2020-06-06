package client.gui;

import client.AzioniJMSListener;
import client.session.Utente;

import java.awt.event.*;
import java.util.Observer;

import javax.swing.*;

public class AzioniListener implements ActionListener {
	private AzioniFrame frameAzioni;
	public static final String COMPRA_CMD = "A";
	public static final String ACCEDI_CMD = "B";

	private AzioniJMSListener jmsListener;

	public AzioniListener(AzioniFrame frameAzioni) {
		this.frameAzioni = frameAzioni;
		this.jmsListener = new AzioniJMSListener(
				new Observer[] {
						frameAzioni,
						frameAzioni.getQuotazioniTableModel()
				}
		);
	}

	public void actionPerformed(ActionEvent e) {
		String com = e.getActionCommand();
		if (com == ACCEDI_CMD)
			autentica();
		else if (com == COMPRA_CMD)
			compra();
	}

	public void autentica() {
		String utente = Utente.getInstance().getUtente();
	
		do {
			utente = (String) JOptionPane
					.showInputDialog(
							this.frameAzioni,
							"Specificare il nome del mittente",
							this.frameAzioni.getTitle(),
							JOptionPane.PLAIN_MESSAGE,
							null,
							null,
							utente
					);
			utente.trim();
		} while (utente != null && utente.equals(""));
		
		if (utente != null) {
			this.frameAzioni.abilitaPulsanteAcquisto(true);
			this.jmsListener.start();
		}
		else
			this.jmsListener.stop();
		
		Utente.getInstance().setUtente(utente);
	}

	public void compra() {
		CompraFrame frameAcquisto = new CompraFrame();

		String nomeAzione = this.frameAzioni.getNomeAzioneSelezionata();
		if (nomeAzione != null) {
			/*
			 * Se viene selezionata una riga della tabella, allora nella finestra
			 * CopraFrame viene aggiornato il campo nomeTxt con il valore sezionato
			 */
			frameAcquisto.setNome(nomeAzione);
		}
		frameAcquisto.setVisible(true);
	}
}