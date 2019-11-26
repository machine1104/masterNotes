
import java.util.Arrays;
import java.util.Base64;
import java.util.Properties;
import java.util.Random;
import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import org.apache.commons.crypto.cipher.CryptoCipher;
import org.apache.commons.crypto.cipher.CryptoCipherFactory;
import org.apache.commons.crypto.cipher.CryptoCipherFactory.CipherProvider;
import org.apache.commons.crypto.utils.Utils;

public class script_java {

    public static byte[] encrypt(byte[] iv, byte[] pw, byte[] msg) {
        try {
            IvParameterSpec iv_spec = new IvParameterSpec(iv);
            SecretKeySpec pw_spec = new SecretKeySpec(pw, "AES");
            Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5PADDING");
            cipher.init(Cipher.ENCRYPT_MODE, pw_spec, iv_spec);
            return cipher.doFinal(msg);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return null;
    }

    
    public static byte[] decrypt(byte[] iv, byte[] pw, byte[] enc_msg) {
        try {
            IvParameterSpec iv_spec = new IvParameterSpec(iv);
            SecretKeySpec pw_spec = new SecretKeySpec(pw, "AES");
            Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5PADDING");
            cipher.init(Cipher.DECRYPT_MODE, pw_spec, iv_spec);
            return cipher.doFinal(enc_msg);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return null;
    }

    public static byte[] encrypt_apache(byte[] iv, byte[] pw, byte[] msg) {
        try {
            IvParameterSpec iv_spec = new IvParameterSpec(iv);
            SecretKeySpec pw_spec = new SecretKeySpec(pw, "AES");
            Properties properties = new Properties();
            properties.setProperty(CryptoCipherFactory.CLASSES_KEY, CipherProvider.OPENSSL.getClassName());
            CryptoCipher cipher = Utils.getCipherInstance("AES/CBC/PKCS5Padding", properties);
            cipher.init(Cipher.ENCRYPT_MODE, pw_spec, iv_spec);
            byte[] out = new byte[msg.length * 2];
            int bytes = cipher.doFinal(msg, 0, msg.length, out, 0);
            return Arrays.copyOf(out, bytes);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return null;
    }
    
    public static byte[] decrypt_apache(byte[] iv, byte[] pw, byte[] enc_msg) {
        try {
            IvParameterSpec iv_spec = new IvParameterSpec(iv);
            SecretKeySpec pw_spec = new SecretKeySpec(pw, "AES");
            Properties properties = new Properties();
            properties.setProperty(CryptoCipherFactory.CLASSES_KEY, CipherProvider.OPENSSL.getClassName());
            CryptoCipher cipher = Utils.getCipherInstance("AES/CBC/PKCS5Padding", properties);
            cipher.init(Cipher.DECRYPT_MODE, pw_spec, iv_spec);
            byte[] out = new byte[enc_msg.length * 2];
            int bytes = cipher.doFinal(enc_msg, 0, enc_msg.length, out, 0);
            return Arrays.copyOf(out, bytes);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return null;
    }

    public static void main(String[] args) {

        Random rd = new Random();
        byte[] iv = new byte[16];
        rd.nextBytes(iv);
        byte[] pw = new byte[32];
        rd.nextBytes(pw);
        int length = (int) Math.pow((double) (10), (double) (8));
        byte[] data = new byte[length];
        rd.nextBytes(data);

        System.out.println("Plaintext: " + Base64.getEncoder().encodeToString(data).substring(0, 100) + "...");
        byte[] ciphertext = encrypt(iv, pw, data);
        System.out.println("Ciphertext with javax.crypto: " + Base64.getEncoder().encodeToString(ciphertext).substring(0, 100) + "...");
        byte[] plaintext = decrypt_apache(iv, pw, ciphertext);
        System.out.println("Decrypted with org.apache.commons.crypto: " + Base64.getEncoder().encodeToString(plaintext).substring(0, 100) + "...");
        System.out.println("Compare 1 = "+ Arrays.equals(data, plaintext) );
        data = new byte[length];
        byte[] ciphertext = encrypt_apache(iv, pw, data);
        System.out.println("Ciphertext with org.apache.commons.crypto: " + Base64.getEncoder().encodeToString(ciphertext).substring(0, 100) + "...");
        byte[] plaintext = decrypt(iv, pw, ciphertext);
        System.out.println("Decrypted with javax.crypto:: " + Base64.getEncoder().encodeToString(plaintext).substring(0, 100) + "...");
        System.out.println("Compare 2 = "+ Arrays.equals(data, plaintext) );
        
        

    }
}
