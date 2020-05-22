% produce vacuum field data for ITER
% for benchmarking with other codes (ERGOS, probe_g, etc.)
% vacuum field from dabase on ITER cluster:
% hpc-login.iter.org:  /work/projects/3D-fields/ITER15MAQ10/DataVac/
% note that vacuum data assumes 1 kAt n=3 coil current in each row

% consider one optimal coil phasing from EvansNF13 paper:
% DeltaPhiU=86, DeltaPhiM=0, DeltaPhiL=34 using Eq. (1) in the paper

kplot = 1; %1: MARS-F n=3 field constructed by Liu, with PHI_ASCOT=[86 0 34]
           %2: MARS-F n=3 field constructed by Heinke, with PHI_ASCOT=[86 0 34]
           %3: Biot-Savart n=3 field calculated by Heinke, with PHI_ASCOT=[86 0 34]
           %4: Biot-Savart n=3 field calculated by Todd, with PHI_ASCOT=[86 0 34] and assuming 90 kAt current

if kplot==1, SS='r-'; end
if kplot==2, SS='b-'; end
if kplot==3, SS='g-'; end
if kplot==4, SS='b-'; end

% convert to MARS-F definition of coil phasing:
n_ASCOT = 3;
phic_ASCOT = [30 26.7 30];
PHI_ASCOT=[86 0 34];
PHI_SHIFT=180;
k = 1;
PHI_MARS = n_ASCOT*(phic_ASCOT-PHI_ASCOT)-PHI_SHIFT+360*k;
% ==> PHI_MARS=[111.9 0 267.9];

% combine three rows of coils with above coil phasing
% fio_comb_field_f.x ==> ~/Work/ITER/Data/BPLASMA_MARSF_n3_cC_VAC.IN

% choose (R,Z) plots to compute n=3 (dBR,dBphi,dBZ) components 
% as complex numbers
% by running: FIO_EVAL_FIELD_CPLX/fio_test.x
data1 = [
%R[m] Z[m]  Re(dBR)         Im(dBR)         Re(dBphi)       Im(dBphi)       Re(dBZ)         Im(dBZ)
 6.2273 0.0571 0.20672703E-04 -0.16700848E-04  0.13401590E-04  0.11985655E-04  0.14878417E-04  0.18882324E-04 %Li's field inclduing wall response, combined
 6.2273 0.0571 0.20654858E-04 -0.16713296E-04  0.13401024E-04  0.11984580E-04  0.14892456E-04  0.18868119E-04 %Liu's field including wall response, direct run
 6.2273 0.0571 0.33757107E-04 -0.68355327E-05  0.62984446E-05  0.22795801E-04  0.70176019E-05  0.25744222E-04 %Liu's field w/o wall response (pure vacuum)
];

% plot fields vs. phi angle
% assuming 90 kAt coil current
phi  = linspace(0,360,361); phi=phi(:);
phi0 = 60; 
fac0= 1.0; 
if kplot==1, Cphi = exp((phi+phi0)*n_ASCOT*i*pi/180)*1e+4*90*fac0; end
if kplot==4, Cphi = exp((phi+30)*n_ASCOT*i*pi/180); end

if kplot==1, d=data1; end
if kplot==2 | kplot==3
   x=load('../Data_VAC/hf_grid.txt');
   if kplot==2, d=load('../Data_VAC/hf_marsf.txt'); end
   if kplot==3, d=load('../Data_VAC/hf_biot.txt'); end
   phi=[x; x(2:end)+120; x(2:end)+240];
   d=[d; d(2:end,:); d(2:end,:)]*10*90;  %Gauss
   if kplot==2, II=phi0; d=[d(II+1:end,:); d(2:II+1,:)]; end  %60 degrees phase shift
   rBR = d(:,1);
   rBP = d(:,3);
   rBZ = d(:,2);
end
if kplot==4
   n = 3;
   d = load('../Data_VAC/probe_gb_TMB.out');
   x = linspace(0,2*pi,361); x=x(1:end-1); x=x(:);
   y = d(:,4:6); 
   yn3 = ones(1,size(y,2));
   for k=1:size(y,2)
       yn3(k) = sum(y(:,k).*exp(-i*n*x));
   end
   yn3 = yn3*x(2)/2/pi*1e+4*2;
end
 
for k=3:3
    if kplot==1
       dBR = d(k,3)+d(k,4)*i;
       dBP = d(k,5)+d(k,6)*i;
       dBZ = d(k,7)+d(k,8)*i;
    end
    if kplot==4
       dBR = yn3(2);
       dBP = yn3(1);
       dBZ = yn3(3);
    end

    if kplot==1 | kplot==4
       rBR = real(dBR*Cphi);
       rBP = real(dBP*Cphi);
       rBZ = real(dBZ*Cphi);
    end

    if kplot==4
       res = [phi rBP rBR rBZ];
       save probe_gb_TMB_n3.out res -ascii -double
    end

    hf=figure(1);
    plot(phi,rBR,SS,'LineWidth',3), 
    xlabel('\phi [degrees]','FontSize',20)
    ylabel('{\delta}B_R [Gauss]','FontSize',20)
    ha = get(hf,'CurrentAxes'); set(ha,'FontSize',20)
    a = axis; axis([0 360 a(3) a(4)])
    hold on,
    print('-f1',['../Resu_3D/VacBr_' int2str(k)],'-depsc')

    hf=figure(2);
    plot(phi,rBP,SS,'LineWidth',3), 
    xlabel('\phi [degrees]','FontSize',20)
    ylabel('{\delta}B_{\phi} [Gauss]','FontSize',20)
    ha = get(hf,'CurrentAxes'); set(ha,'FontSize',20)
    a = axis; axis([0 360 a(3) a(4)])
    hold on,
    print('-f2',['../Resu_3D/VacBphi_' int2str(k)],'-depsc')

    hf=figure(3);
    plot(phi,rBZ,SS,'LineWidth',3), 
    xlabel('\phi [degrees]','FontSize',20)
    ylabel('{\delta}B_Z [Gauss]','FontSize',20)
    ha = get(hf,'CurrentAxes'); set(ha,'FontSize',20)
    a = axis; axis([0 360 a(3) a(4)])
    hold on,
    print('-f3',['../Resu_3D/VacBz_' int2str(k)],'-depsc')
end






