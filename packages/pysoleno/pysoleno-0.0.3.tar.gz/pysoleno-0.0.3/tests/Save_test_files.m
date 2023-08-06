%% target points
r_d = 100;
z_d = 100;
R = linspace(-0.4,0.4,r_d);
Z = linspace(-0.4,0.4,z_d);

[R2,Z2] = meshgrid(R,Z);

% Definition of magnet
Rin = [0.13,0.13];
Rout = [0.15,0.15];
Zlow = [-0.1,0.05];
Zhigh = [-0.05,0.1];

Nturn = [200,200];
I = [200,200];
Nloop = [6,6];
Itot = Nturn.*I;


%% Calculation
[Br,Bz] = soleno_calcB(R2,Z2,Rin,Rout,Zlow,Zhigh,Itot,Nloop);
M_magnet = soleno_calcM(Rin,Rout,Zlow,Zhigh,Nturn,Nloop);

%disp('Inductance Matrix');
%disp(M_magnet);
%% Save to output files
test = "test1";
folder = pwd+"\"+ test;

% Magnet file
output_file = folder + ".magnet";
fileID = fopen(output_file, 'w');
        % Header
        fprintf(fileID,'%s %s %s %s %s %s %s',['Rin(m) ', 'Rout(m) ', 'Zlow(m) ', 'Zhigh(m) ', 'I(A) ', 'Nturn(-) ', 'Nloop(-) ']);
        fprintf(fileID,'\n');
        % Data
        fprintf(fileID,'%6.8f %6.8f %6.8f %6.8f %6.8f %d %d\n', [Rin', Rout', Zlow', Zhigh', I', Nturn', Nloop']');
        fclose(fileID);

% Field file
output_file = folder + ".field";
fileID = fopen(output_file, 'w');
    % Header
    fprintf(fileID,'%s %s %s %s',['r(mm) ', 'z(mm) ', 'Br(T) ', 'Bz(T)']);
    fprintf(fileID,'\n');
    % Data
    fprintf(fileID,'%6.8f %6.8f %6.8f %6.8f\n', [reshape(R2,1,[])', reshape(Z2,1,[])', reshape(Br,1,[])', reshape(Bz,1,[])']');
fclose(fileID);

% Inductance file
output_file = folder + ".inductance";
fileID = fopen(output_file, 'w');
    % Header
    %fprintf(fileID,'%s\n','Extended self mutual inductance matrix [H/m]');
    fprintf(fileID,'L%d ', [1:length(Rin)]);
    fprintf(fileID,'\n');
    % Data
    for r=1:length(Rin)
        for c=1:length(Rin)
            fprintf(fileID,'%6.8f ', M_magnet(r,c));
        end
        fprintf(fileID,'\n');
    end
fclose(fileID);