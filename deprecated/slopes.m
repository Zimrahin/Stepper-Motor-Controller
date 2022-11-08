n_step = 0;

N = 300;

Pa = 100;
Tas = 1000;
Tai = 600;
Tmin = 600;

if N < 2*Pa
    m1 = slope(0,Tas,Pa,Tai);
    b1 = intercept(0,Tas,m1);
    m2 = slope(N/2,m1*(N/2)+b1,N,Tas);
    b2 = intercept(N,Tas,m2);
else
    m1 = slope(0,Tas,Pa,Tai);
    b1 = intercept(0,Tas,m1);
    m2 = slope(N-Pa,Tai,N,Tas);
    b2 = intercept(N-Pa,Tai,m2);
end

figure;
hold on
while n_step < 2*N
    x = n_step/2;
    if N < 2*Pa
        if x < N/2
            interval = m1*x + b1;
        else 
            interval = m2*x + b2;
        end
    else
        if x < Pa
            interval = m1*x + b1;
        else 
            if x < N - Pa
                interval = Tai;
            else
                interval = m2*x + b2;  
            end
        end
    end
    scatter(n_step,interval,'filled','b');
    n_step = n_step + 1;
end


%%
function m = slope(x1,y1,x2,y2)
    m = (y2 - y1)/(x2 - x1);
end

function i = intercept(x1,y1,m)
    i = y1 - m*x1;
end