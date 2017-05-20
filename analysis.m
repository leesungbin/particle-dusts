% make origin data
% ~0.4 d:1.24mm 5.53m/s 280drops/s m^2
% 0.4~1.5 d:1.60mm 6.28m/s 495drops/s m^2
% 1.5~6.0 d:2.05mm 7.11m/s 495drops/s m^2
% 6.0~16.0 d:2.40 7.69m/s 818drops/s m^2
% 16.0~ d:2.85 8.38m/s 1220drops/s m^2r=0.001443;
% Nr=94;
% Nr, tf, Vpath,v

%constants
h=2000;


rho_w=1000;
rho_a=((-0.0977*2+1.225)+1.225)/2;
Cd=0.47;

g=9.80;
%==
r=[];
v=[];
tf=[];
Nr=[];
Nr_m3=[];
a=[];
b=[];
k=[];
Vpath=[];
t90=[];

%over 20
for i =1:length(pm10.hr)
    %if pm10.pm10(i)>50
        x=pm10.power(i);
        if x<=0.4
            r(i)=1.24/2/1000;
            v(i)=5.53;
            Nr(i)=280;
        elseif x<=1.5
            r(i)=1.60/2/1000;
            v(i)=6.28;
            Nr(i)=495;
        elseif x<=6.0
            r(i)=2.05/2/1000;
            v(i)=7.11;
            Nr(i)=495+(828-495)*(x-1.5)/(6.0-1.5);
        elseif x<=16.0
            r(i)=2.40/2/1000;
            v(i)=7.69;
            Nr(i)=818+(1220-818)*(x-6)/(16-6);
        else
            r(i)=2.85/2/1000;
            v(i)=8.38;
            Nr(i)=1220;
        end
        %Nr_m3(i)=Nr(i)/v(i);
        V(i)=4/3*pi*r(i)^3;
        A(i)=pi*r(i)^2;
        mass(i)=V(i)*rho_w;
        v(i)=sqrt(mass(i)*g/(1/2*rho_a*Cd*A(i)));
        tf(i)=h/v(i);
        Vpath(i)=pi*r(i)^2*v(i);
        
        b(i)=log((pm10.pm10(i)+pm10.delta(i))/pm10.pm10(i))/(-1*pm10.hr(i)*3600);
        a(i)=pm10.pm10(i);
        k(i)=b(i)/(Nr(i)*Vpath(i));
        t90(i)=log(0.1)/-b(i)/3600/24;
    %end
end
% 
% count=0;
% for i = 1:length(t90)
%     if t90(i)>9.14
%         count=count+1;
%     elseif t90(i)<1.39
%         count=count+1;
%     end
% end
% count
% 
% badpm=0;
% bpmt=[];
% for i =1:length(t90)
%     if pm10.pm10(i)>80
%         badpm=badpm+1;
%         bpmt(badpm)=t90(i);
%     end
% end
% mean(bpmt)


% for i =[1:length(Nr)]
%     trange=0:.1:tf(i);
%     y1=2000*pm10.pm10(i)*exp(-Nr(i)*pi*r(i)^2*v(i)*0.0012*1/2.*trange.^2);
%     y2=
% end