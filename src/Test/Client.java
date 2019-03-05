package Test;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.Socket;

public class Client {

    public static final String IP = "172.22.250.101";//��������ַ
    public static final int PORT = 5209;//�������˿ں�
    ReadHandlerThread listenFromClient;
    WriteHandlerThread writeToClient;


    public static void main(String[] args) {
        Client server = new Client();
        server.init();
    }

    private void init(){
        try {
            //ʵ����һ��Socket����ָ����������ַ�Ͷ˿�
            Socket client = new Socket(IP, PORT);
            //���������̣߳�һ���������һ������д
            listenFromClient = new ReadHandlerThread(client);
            listenFromClient.start();

            writeToClient = new WriteHandlerThread(client);
            writeToClient.start();
            while(true) {
                // ����¼��
                BufferedReader br =
                        new BufferedReader(new InputStreamReader(System.in));
                writeToClient.writeTo(br.readLine());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
