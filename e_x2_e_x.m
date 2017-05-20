
sym f1(x)
sym f2(x)
f1(x)=exp(-1/2*x^2);
f2(x)=exp(-x);
range=0:.1:10;
plot(range,f1(range))
hold on
plot(range,f2(range))

diff(f1,x,2)