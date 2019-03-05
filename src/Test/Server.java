package Test;


import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

public class Server {

    public static final int PORT = 8000;//�����Ķ˿ں�
    ReadHandlerThread listenFromClient;
    WriteHandlerThread writeToClient;

    public static void main(String[] args) {
        Server server = new Server();
        server.init();
    }

    public void init() {
        ServerSocket serverSocket = null;
        try {
            serverSocket = new ServerSocket(PORT);
            while (true) {
                Socket client = serverSocket.accept();
                //һ���ͻ������ӾͿ��������̴߳����д
                listenFromClient = new ReadHandlerThread(client);
                listenFromClient.start();

                writeToClient = new WriteHandlerThread(client);
                writeToClient.start();
                while(true) {
                    //System.out.println("�߳���:" + listenFromClient.readFrom());
                    // ����¼��
                    BufferedReader br =
                            new BufferedReader(new InputStreamReader(System.in));
                    writeToClient.writeTo(br.readLine());
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally{
            try {
                if(serverSocket != null){
                    serverSocket.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}

/*
 *������������߳�
 */
class ReadHandlerThread extends Thread{
    private Socket client;
    private volatile String receivedMsg;
    private volatile boolean ready;

    public ReadHandlerThread(Socket client) {
        this.client = client;
        ready = false;
    }
    public String readFrom(){
        //while(!ready){}
        String  result = receivedMsg;
        ready = false;
        return result;
    }

    @Override
    public void run() {
        DataInputStream dis = null;
        try{
            while(true){
                //��ȡ�ͻ�������
                dis = new DataInputStream(client.getInputStream());
                String reciver = dis.readUTF();
                receivedMsg = reciver;
                System.out.println("�߳���:" + reciver);
                ready = true;

            }
        }catch(Exception e){
            e.printStackTrace();
        }finally{
            try {
                if(dis != null){
                    dis.close();
                }
                if(client != null){
                    client = null;
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}

/*
 * ����д�������߳�
 */
class WriteHandlerThread extends Thread{
    private Socket client;
    private volatile boolean ready;
    private volatile String msg = null;

    public WriteHandlerThread(Socket client) {
        this.client = client;
        ready = false;
    }

    public void writeTo(String s) {
        msg = s;
        ready = true;
    }
    @Override
    public void run() {
        DataOutputStream dos = null;
        BufferedReader br = null;
        try{
            while(true){
                //��ͻ��˻ظ���Ϣ
                dos = new DataOutputStream(client.getOutputStream());
                System.out.print("������:\n");

                while(ready==false){}

                //��������
                dos.writeUTF(msg);
                ready = false;
            }
        }catch(Exception e){
            e.printStackTrace();
        }finally{
            try {
                if(dos != null){
                    dos.close();
                }
                if(br != null){
                    br.close();
                }
                if(client != null){
                    client = null;
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}