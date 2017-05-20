% f1=@(x) exp(-1/2.*x.^2);
% f2=@(x) exp(-x);
% 
syms f1(x)
syms f2(x)
f1(x)=2000*100*exp(-200*pi*0.0011^2*0.0011*1/2*x^2);
f2(x)=2000*100*exp(-200*pi*0.0011^2*0.0011*x);
range=0:1:30000;
plot(range,f1(range))
hold on
plot(range,f2(range))
hold off
% diff(f1,x,2)
% integrate(f1,x,0,266)