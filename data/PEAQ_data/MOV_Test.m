Files = {'timeAligned_mic1.wav','timeAligned_mic2.wav',...
         'timeAligned_mic3.wav','timeAligned_piezo.wav';
         'timeAligned_mic1_10sec.wav','timeAligned_mic2_10sec.wav',...
         'timeAligned_mic3_10sec.wav','timeAligned_piezo_10sec.wav';
         'timeAligned_mic1_25sec.wav','timeAligned_mic2_25sec.wav',...
         'timeAligned_mic3_25sec.wav','timeAligned_piezo_25sec.wav'};
     
num_timeFrames = size(Files,1);
num_recTypes = size(Files,2);

title_MOV = 'MOV_';
title_ODG = 'ODG_';

param_names = {'BandwidthRefB','BandwidthTestB','TotalNMRB','WinModDiff1B',...
               'ADBB','EHSB','AvgModDiff1B','AvgModDiff2B','RmsNoiseLoudB',...
               'MFPDB','RelDistFramesB','ODG'};

timeFrames = {'1 second','10 seconds','25 seconds'};

num_params = length(param_names);

BandwidthRefB = zeros(num_recTypes,num_recTypes);
BandwidthTestB = zeros(num_recTypes,num_recTypes);
TotalNMRB = zeros(num_recTypes,num_recTypes);
WinModDiff1B = zeros(num_recTypes,num_recTypes);
ADBB = zeros(num_recTypes,num_recTypes);
EHSB = zeros(num_recTypes,num_recTypes);
AvgModDiff1B = zeros(num_recTypes,num_recTypes);
AvgModDiff2B = zeros(num_recTypes,num_recTypes);
RmsNoiseLoudB = zeros(num_recTypes,num_recTypes);
MFPDB = zeros(num_recTypes,num_recTypes);
RelDistFramesB = zeros(num_recTypes,num_recTypes);
ODG_matrix = zeros(num_recTypes,num_recTypes);

BandwidthRefB_total = cell(num_timeFrames,1);
BandwidthTestB_total = cell(num_timeFrames,1);
TotalNMRB_total = cell(num_timeFrames,1);
WinModDiff1B_total = cell(num_timeFrames,1);
ADBB_total = cell(num_timeFrames,1);
EHSB_total = cell(num_timeFrames,1);
AvgModDiff1B_total = cell(num_timeFrames,1);
AvgModDiff2B_total = cell(num_timeFrames,1);
RmsNoiseLoudB_total = cell(num_timeFrames,1);
MFPDB_total = cell(num_timeFrames,1);
RelDistFramesB_total = cell(num_timeFrames,1);
ODG_total = cell(num_timeFrames,1);

for row = 1:num_timeFrames
    for m = 1:num_recTypes
        for n = 1:num_recTypes
            FileIn = Files{row,m};
            FileOut = Files{row,n};
            
            [ODG, MOV] = PQevalAudio_fn(FileIn,FileOut);
            
            BandwidthRefB(m,n) = MOV(1);
            BandwidthTestB(m,n) = MOV(2); 
            TotalNMRB(m,n) = MOV(3); 
            WinModDiff1B(m,n) = MOV(4);
            ADBB(m,n) = MOV(5); 
            EHSB(m,n) = MOV(6); 
            AvgModDiff1B(m,n) = MOV(7); 
            AvgModDiff2B(m,n) = MOV(8); 
            RmsNoiseLoudB(m,n) = MOV(9); 
            MFPDB(m,n) = MOV(10); 
            RelDistFramesB(m,n) = MOV(11); 
            ODG_matrix(m,n) = ODG;
 
        end
    end
    
    BandwidthRefB_total{row,1} = BandwidthRefB;
    BandwidthTestB_total{row,1} = BandwidthTestB;
    TotalNMRB_total{row,1} = TotalNMRB;
    WinModDiff1B_total{row,1} = WinModDiff1B;
    ADBB_total{row,1} = ADBB;
    EHSB_total{row,1} = EHSB;
    AvgModDiff1B_total{row,1} = AvgModDiff1B;
    AvgModDiff2B_total{row,1} = AvgModDiff2B;
    RmsNoiseLoudB_total{row,1} = RmsNoiseLoudB;
    MFPDB_total{row,1} = MFPDB;
    RelDistFramesB_total{row,1} = RelDistFramesB;
    ODG_total{row,1} = ODG_matrix;
    
    BandwidthRefB = zeros(num_recTypes,num_recTypes);
    BandwidthTestB = zeros(num_recTypes,num_recTypes);
    TotalNMRB = zeros(num_recTypes,num_recTypes);
    WinModDiff1B = zeros(num_recTypes,num_recTypes);
    ADBB = zeros(num_recTypes,num_recTypes);
    EHSB = zeros(num_recTypes,num_recTypes);
    AvgModDiff1B = zeros(num_recTypes,num_recTypes);
    AvgModDiff2B = zeros(num_recTypes,num_recTypes);
    RmsNoiseLoudB = zeros(num_recTypes,num_recTypes);
    MFPDB = zeros(num_recTypes,num_recTypes);
    RelDistFramesB = zeros(num_recTypes,num_recTypes);
    ODG_matrix = zeros(num_recTypes,num_recTypes);
end

% col_header={'Mic 1','Mic 2','Mic 3','Piezo'}; %Row cell array (for column labels)
% row_header={'Mic 1';'Mic 2';'Mic 3';'Piezo'}; %Column cell array (for row labels)
% 
% cells_sect_header = {'C1','I1','O1'};
% cells_data = {'B3','H3','N3'};
% cells_col_header = {'B2','H2','N2'};
% cells_row_header = {'A3','G3','M3'};
% 
% for j = 1:num_params
%     filename = param_names{j};
%     for k = 1:num_timeFrames
%         data_expression = strcat(param_names{j},'_total{',num2str(k),',1};');
%         curr_data = eval(data_expression);
%         section_header = strcat(param_names{j},' (',timeFrames{k},')');
%         
%         curr_row_cell = cells_row_header{k}
%         curr_col_cell = cells_col_header{k}
%         curr_sect_cell = cells_sect_header{k}
%         curr_data_cell = cells_data{k}
%         
%         xlswrite(filename,section_header,'Sheet1',curr_sect_cell); %Write section header
%         xlswrite(filename,col_header,'Sheet1',curr_col_cell);     %Write column header
%         xlswrite(filename,row_header,'Sheet1',curr_row_cell);      %Write row header
%         xlswrite(filename,curr_data,'Sheet1',curr_data_cell);     %Write data
%     end
% end

for j = 1:num_params
    filename = param_names{j};
    
    data_expression1 = strcat(param_names{j},'_total{1,1};');
    data_expression2 = strcat(param_names{j},'_total{2,1};');
    data_expression3 = strcat(param_names{j},'_total{3,1};');
    
    curr_data1 = eval(data_expression1);
    curr_data2 = eval(data_expression2);
    curr_data3 = eval(data_expression3);
    
    curr_data = [curr_data1, curr_data2, curr_data3];
    
    xlswrite(filename,curr_data);     %Write data
end
