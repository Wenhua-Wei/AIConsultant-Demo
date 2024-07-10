import { DefaultEventsMap } from '@socket.io/component-emitter';
import { Socket, io } from 'socket.io-client';
import { StringLiteralLike } from 'typescript';

class WebSocketService {
    private socket: Socket<DefaultEventsMap, DefaultEventsMap> | undefined;

    private messageHandler: ((message: string) => void) | null = null;
    private listHandler: ((message: string) => void) | null = null;
    private popHandler: (() => void) | null = null;
    private loadGeneralQuestion: (() => void) | null = null;
    private recoveryhandler: (() => void) | null = null;
    private stephandler: (() => void) | null = null;
    public isConnected: boolean = false;
    public test = null;
    // ws://localhost:5200
    connect(telephone?: string) {
        this.socket = io('wss://api.consultant.ai4c.cn', {
            transports: ['websocket'],
            autoConnect: true,
            reconnection: true,
            reconnectionAttempts: 3,
            reconnectionDelay: 1000,
            query: {
                telephone: telephone
            }
        });
        // this.socket = io('ws://localhost:5200', {
        //     transports: ['websocket'],
        //     autoConnect: true,
        //     reconnection: true,
        //     reconnectionAttempts: 3,
        //     reconnectionDelay: 1000,
        //     query: {
        //         telephone: telephone
        //     }
        // });

        this.socket.on('connect', () => {
            this.isConnected = true;
        });


        this.socket.on('error', (data) => {
            console.error('WebSocket Error', data);
            this.isConnected = false;
        });


        this.socket.on('close', (data) => {
            console.log(data);
        });


        this.socket.on('server-message', (message) => {
            if (this.messageHandler) {
                this.messageHandler(message);
            }
        });

        this.socket.on('message-over', () => {
            if (this.recoveryhandler)
                this.recoveryhandler();
        });

        this.socket.on('list', (message) => {
            if (this.listHandler) {
                console.log(message)
                this.listHandler(message);
            }
        });

        this.socket.on('info-collected', () => {
            if (this.popHandler) {
                this.popHandler();
                if (telephone) {
                    this.notifyDataReady(telephone)
                }
            }
        });

        this.socket.on('loadGeneralQuestion', () => {
            if (this.loadGeneralQuestion) {
                this.loadGeneralQuestion();
            }
        });

        this.socket.on('readyforaddQuestion',()=>{
            if(this.popHandler){
                this.popHandler();
            }
        })

        this.socket.on('setstep',()=>{
            if(this.stephandler){
                this.stephandler();
            }
        })
    }

    sendMessage(data: { user_message: string; purpose: string; telephone: String }) {
        if (!this.socket) {
            console.error('WebSocket is not connected.');
            return;
        }


        if (this.isConnected) {
            this.socket.send(data);
        } else {
            console.error('WebSocket is not ready to send message.');
        }
    }

    notifyDataReady(telephone: string) {
        if (this.socket && this.isConnected) {
            this.socket.emit('data-ready', { message: 'Frontend is ready for the next data step', telephone: telephone });
        }
    }


    disconnect() {
        if (!this.socket) return;
        this.socket.close();
        this.isConnected = false;
    }

    setMessageHandler(handler: (message: string) => void) {
        this.messageHandler = handler;
    }

    setPopHandle(handler: () => void) {
        this.popHandler = handler;
    }

    setlistHandler(handler: (message: string) => void) {
        this.listHandler = handler;
    }

    sendTelephone(telephone: string) {
        if (this.socket && this.isConnected) {
            this.socket.emit('sendTelephone', { telephone });
        }
    }

    setRecoveryHandle(handler: () => void) {
        this.recoveryhandler = handler;
    }

    setStepHandler(handler:()=>void){
        this.stephandler=handler;
    }

    beforeConnected(handler: () => void) {
        this.loadGeneralQuestion = handler;
    }


} export const webSocketService = new WebSocketService();

