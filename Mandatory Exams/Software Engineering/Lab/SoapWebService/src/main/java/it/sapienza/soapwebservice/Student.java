package it.sapienza.soapwebservice;

import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;

/**
 *
 * @author studente
 */
@XmlJavaTypeAdapter(StudentAdapter.class)
public interface Student {

    public String getName();
}
