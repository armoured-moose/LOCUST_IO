% produce vacuum field data for ITER w/o RW response
% for benchmarking withprobe_g
% MARS-F vacuum data are stored in: ../Data_VAC
% note that vacuum data assumes 1 kAt n=3 or n=6 coil current in each row w/o In/Ic factor
% consider one optimal coil phasing from EvansNF13 paper:
% DeltaPhiU=86, DeltaPhiM=0, DeltaPhiL=34 using Eq. (1) in the paper
% compare field along phi-angle at R=6.2273m, Z=0.0571m
% compare both the n=3 main harmonic and the n=6 sideband field

% convert to MARS-F definition of coil phasing:
n_ASCOT = 3;
phic_ASCOT = [30 26.7 30];
PHI_ASCOT=[86 0 34];
PHI_SHIFT=180;
k = 1;
PHI_MARS = n_ASCOT*(phic_ASCOT-PHI_ASCOT)-PHI_SHIFT+360*k;
PHI_MARS = PHI_MARS - PHI_MARS(2);
PHI_MARS([1 3]) = PHI_MARS([1 3]) + 360;
% ==> PHI_MARS=[111.9 0 267.9];

% get vacuum field from each row of coils at (R,Z)
% FIO_EVAL_FIELD_CPLX/fio_test.x ==> data0 below
% assume 1kAt currentt per row w/o RW, w/o In/Ic factor
data0_n3_V = [
%Re(B_R)        Im(B_R)         Re(Bphi)        Im(Bphi)        Re(B_Z)         Im(B_Z)      
0.57865387E-05  0.36730866E-16 -0.10698996E-15  0.10890207E-04  0.14486468E-04  0.10227762E-15  %U
0.71598882E-04  0.11469550E-15 -0.24859318E-17  0.52280031E-04  0.20087279E-04  0.20979606E-15  %M
0.15210121E-04  0.70365481E-16 -0.31805307E-15  0.19037078E-04 -0.24623779E-04 -0.10433730E-16  %L
];
data0_n6_V = [
%Re(B_R)        Im(B_R)         Re(Bphi)        Im(Bphi)        Re(B_Z)         Im(B_Z)      
0.37564248E-05 -0.65616162E-18  0.11678465E-16  0.62478631E-05  0.63687428E-05  0.43718308E-17  %U
0.49043808E-04 -0.15219669E-16 -0.27875665E-17  0.42481952E-04  0.10532992E-04  0.72137744E-17  %M
0.11458338E-04 -0.28802074E-17 -0.14583073E-16  0.14619530E-04 -0.13670587E-04 -0.66732591E-17  %L
];

% In/Ic factors for n=3 and n=6 fields
fac_InIc = [
%n   fU      fM      fL
 3   0.6645  0.4968  0.6840
 6   0.4772  0.4243  0.4773
];

% linear superposition of U+M+L with proper In/Ic factor and proper coil phasing
% and store results in data1 below
% n=3 main harmonic
fac = fac_InIc(1,2:4); fac = fac(:);
PHI = PHI_MARS(:);
BR  = data0_n3_V(:,1)+i*data0_n3_V(:,2);
BP  = data0_n3_V(:,3)+i*data0_n3_V(:,4);
BZ  = data0_n3_V(:,5)+i*data0_n3_V(:,6);

BRn3 = sum(fac.*BR.*exp(i*PHI/180*pi));
BPn3 = sum(fac.*BP.*exp(i*PHI/180*pi));
BZn3 = sum(fac.*BZ.*exp(i*PHI/180*pi));
res  = [real(BRn3) imag(BRn3) real(BPn3) imag(BPn3) real(BZn3) imag(BZn3)];

% n=6 main harmonic
fac = fac_InIc(2,2:4); fac = fac(:);
PHI =-9*phic_ASCOT(:) - PHI_MARS(:);  
BR  = data0_n6_V(:,1)+i*data0_n6_V(:,2);
BP  = data0_n6_V(:,3)+i*data0_n6_V(:,4);
BZ  = data0_n6_V(:,5)+i*data0_n6_V(:,6);

BRn6 = sum(fac.*BR.*exp(i*PHI/180*pi));
BPn6 = sum(fac.*BP.*exp(i*PHI/180*pi));
BZn6 = sum(fac.*BZ.*exp(i*PHI/180*pi));
res  = [real(BRn6) imag(BRn6) real(BPn6) imag(BPn6) real(BZn6) imag(BZn6)];

%combined U+M+L vacuum field
data1 = [
%n  Re(dBR)      Im(dBR)      Re(dBphi)    Im(dBphi)    Re(dBZ)      Im(dBZ)
 3  3.3755e-05  -6.8291e-06   6.2983e-06   2.2796e-05   7.0061e-06   2.5763e-05
 6 -1.4112e-05   1.7207e-05  -1.4289e-05  -1.3138e-05   7.1262e-06   2.9876e-06
];

% get B-field along phi
% assuming 90 kAt coil current
% note that the phi-angle below should correspond to the absolute phi-angle as defined in ITER
phi  = linspace(0,360,361); phi=phi(:);  phi0 = 30; 
Cphi = exp((phi+phi0)*n_ASCOT*i*pi/180)*1e+4*90; 
rBRn3  = real(BRn3*Cphi);
rBPn3  = real(BPn3*Cphi);
rBZn3  = real(BZn3*Cphi);

Cphi = exp((phi+phi0)*6*i*pi/180)*1e+4*90; 
rBRn6  = real(BRn6*Cphi);
rBPn6  = real(BPn6*Cphi);
rBZn6  = real(BZn6*Cphi);

%plot vacuum field from MARS-F
SS   = 'r-';

hf=figure(1);
plot(phi,rBRn3,SS,'LineWidth',3), 
xlabel('\phi [degrees]','FontSize',20)
ylabel('n=3 {\delta}B_R [Gauss]','FontSize',20)
ha = get(hf,'CurrentAxes'); set(ha,'FontSize',20)
a = axis; axis([0 360 a(3) a(4)])
hold on;
%print('-f1',['../Resu_3D/VacBr_' int2str(k)],'-depsc')

hf=figure(2);
plot(phi,rBPn3,SS,'LineWidth',3), 
xlabel('\phi [degrees]','FontSize',20)
ylabel('n=3 {\delta}B_{\phi} [Gauss]','FontSize',20)
ha = get(hf,'CurrentAxes'); set(ha,'FontSize',20)
a = axis; axis([0 360 a(3) a(4)])
hold on;
%print('-f2',['../Resu_3D/VacBphi_' int2str(k)],'-depsc')

hf=figure(3);
plot(phi,rBZn3,SS,'LineWidth',3), 
xlabel('\phi [degrees]','FontSize',20)
ylabel('n=3 {\delta}B_Z [Gauss]','FontSize',20)
ha = get(hf,'CurrentAxes'); set(ha,'FontSize',20)
a = axis; axis([0 360 a(3) a(4)])
hold on;
%print('-f3',['../Resu_3D/VacBz_' int2str(k)],'-depsc')

hf=figure(4);
plot(phi,rBRn6,SS,'LineWidth',3), 
xlabel('\phi [degrees]','FontSize',20)
ylabel('n=6 {\delta}B_R [Gauss]','FontSize',20)
ha = get(hf,'CurrentAxes'); set(ha,'FontSize',20)
a = axis; axis([0 360 a(3) a(4)])
hold on;
%print('-f1',['../Resu_3D/VacBr_' int2str(k)],'-depsc')

hf=figure(5);
plot(phi,rBPn6,SS,'LineWidth',3), 
xlabel('\phi [degrees]','FontSize',20)
ylabel('n=6 {\delta}B_{\phi} [Gauss]','FontSize',20)
ha = get(hf,'CurrentAxes'); set(ha,'FontSize',20)
a = axis; axis([0 360 a(3) a(4)])
hold on;
%print('-f2',['../Resu_3D/VacBphi_' int2str(k)],'-depsc')

hf=figure(6);
plot(phi,rBZn6,SS,'LineWidth',3), 
xlabel('\phi [degrees]','FontSize',20)
ylabel('n=6 {\delta}B_Z [Gauss]','FontSize',20)
ha = get(hf,'CurrentAxes'); set(ha,'FontSize',20)
a = axis; axis([0 360 a(3) a(4)])
hold on;
%print('-f3',['../Resu_3D/VacBz_' int2str(k)],'-depsc')


% get vacuum field from probe_g data
% perform Fourier decomposition along phi for n=3 and n=6 components
d = load('probe_gb_TMB.out');
y = d(:,4:6); 
x = linspace(0,2*pi,size(y,1)); x=x(1:end-1); x=x(:);
yn3 = ones(1,size(y,2));
yn6 = ones(1,size(y,2));
for k=1:size(y,2)
    yn3(k) = sum(y(:,k).*exp(-i*3*x));
    yn6(k) = sum(y(:,k).*exp(-i*6*x));
end
yn3 = yn3*x(2)/2/pi*1e+4*2;
yn6 = yn6*x(2)/2/pi*1e+4*2;

Cphi = exp(phi*n_ASCOT*i*pi/180); 
rBRn3 = real(yn3(2)*Cphi);
rBPn3 = real(yn3(1)*Cphi);
rBZn3 = real(yn3(3)*Cphi);

Cphi = exp(phi*6*i*pi/180); 
rBRn6 = real(yn6(2)*Cphi);
rBPn6 = real(yn6(1)*Cphi);
rBZn6 = real(yn6(3)*Cphi);

%plot vacuum field from probe_g
SS   = 'b-';

hf=figure(1);
plot(phi,rBRn3,SS,'LineWidth',3), 
hold on;

hf=figure(2);
plot(phi,rBPn3,SS,'LineWidth',3), 
hold on;

hf=figure(3);
plot(phi,rBZn3,SS,'LineWidth',3), 
hold on;

hf=figure(4);
plot(phi,rBRn6,SS,'LineWidth',3), 
hold on;

hf=figure(5);
plot(phi,rBPn6,SS,'LineWidth',3), 
hold on;

hf=figure(6);
plot(phi,rBZn6,SS,'LineWidth',3), 
hold on;







