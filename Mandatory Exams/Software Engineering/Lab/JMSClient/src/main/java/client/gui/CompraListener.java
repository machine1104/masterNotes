package client.gui;


import client.CompraJMSManager;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.FocusEvent;
import java.awt.event.FocusListener;

public class CompraListener implements FocusListener, ActionListener {
	private CompraFrame frame;
	private CompraJMSManager compraMan;

	public CompraListener(CompraFrame compraFrame) {
		this.frame = compraFrame;
		this.compraMan = new CompraJMSManager(compraFrame);
	}

	public void focusGained(FocusEvent e) { /* DEVE RIMANERE VUOTO */
	}

	public void focusLost(FocusEvent e) {
		try {
			String quantitaTxt = this.frame.getQuantita();
			String prezzoTxt = this.frame.getPrezzo();
			
			int quantita = Integer.parseInt(quantitaTxt);
			float prezzo = Float.parseFloat(prezzoTxt);
			
			// formatta il numero in modo tale che compaiano due cifre decimali
			String finale = String.format("%1$.2f", quantita * prezzo);
			
			this.frame.impostaImportoComplessivo(finale);
		} catch (NumberFormatException err) {
			this.frame.impostaImportoComplessivo("0.00");
		}
	}

	public void actionPerformed(ActionEvent ae) {
		boolean buonEsito = false;
		try {
			buonEsito = this.compraMan.compra(
					this.frame.getNome(),
					Float.parseFloat(this.frame.getPrezzo()),
					Integer.parseInt(this.frame.getQuantita())
				);
			if (!buonEsito) {
				this.frame.notificaErrore(
						"La transazione non \u00e8 andata a buon fine."
					);
			}
		} catch (NumberFormatException nFE) {
			this.frame.notificaErrore(
					"Quantit\u00e0 e prezzo devono essere valori numerici, " +
					"risp. intero e decimale"
				);
		}
	}
}