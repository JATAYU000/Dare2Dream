% Clear everything before loading
clc;
clear ALL;
pause on;

% Loading DLL library
if ~libisloaded('Thinkgear')
    loadlibrary('thinkgear64.dll');
else
    unloadlibrary Thinkgear
    loadlibrary('thinkgear64.dll');
end
disp('Libraries loaded successfully.');

% File path for saving data
path = 'C:/Users/Rihaa/Documents/MATLAB/bci/';

% Initialize data storage (pre-allocate some space)
data = ones(10000, 14);  % 10,000 rows initially, expands dynamically

% COM port setup
portnum1 = 7;   % COM Port #
comPortName1 = sprintf('\\\\.\\COM%d', portnum1);

% ThinkGear Constants
TG_BAUD_115200 = 115200;
TG_STREAM_PACKETS = 0;

% EEG Data Types
TG_DATA_POOR_SIGNAL = 1;
TG_DATA_ATTENTION = 2;
TG_DATA_MEDITATION = 3;
TG_DATA_RAW = 4;
TG_DATA_DELTA = 5;
TG_DATA_THETA = 6;
TG_DATA_ALPHA1 = 7;
TG_DATA_ALPHA2 = 8;
TG_DATA_BETA1 = 9;
TG_DATA_BETA2 = 10;
TG_DATA_GAMMA1 = 11;
TG_DATA_GAMMA2 = 12;
TG_DATA_BLINK_STRENGTH = 37;

% Get a connection ID
connectionId1 = calllib('Thinkgear', 'TG_GetNewConnectionId');
if (connectionId1 < 0)
    calllib('Thinkgear', 'TG_FreeConnection', connectionId1);
    error(sprintf('ERROR: TG_GetNewConnectionId() returned %d.\n', connectionId1));
end

% Attempt to connect
errCode = calllib('Thinkgear', 'TG_Connect', connectionId1, comPortName1, TG_BAUD_115200, TG_STREAM_PACKETS);
if (errCode < 0)
    calllib('Thinkgear', 'TG_FreeConnection', connectionId1);
    error(sprintf('ERROR: TG_Connect() returned %d.\n', errCode));
end

fprintf('Connected. Reading Packets... Press "Stop" button to stop.\n');

% Stop button GUI
fig = uifigure('Name', 'Stop ThinkGear Data Collection', 'Position', [100 100 300 100]);
btn = uibutton(fig, 'Text', 'Stop', 'Position', [100 30 100 40], ...
               'ButtonPushedFcn', @(btn, event) setappdata(fig, 'stop_flag', true));

% Start data collection
setappdata(fig, 'stop_flag', false);
i = 1; % Row index for data storage

while ~getappdata(fig, 'stop_flag')  % Run until stop button is pressed
    if (calllib('Thinkgear', 'TG_ReadPackets', connectionId1, 1) == 1)  % If a packet is read
        for j = 1:14
            if j == 1
                data(i, j) = now;  % Timestamp
            else
                if (calllib('Thinkgear', 'TG_GetValueStatus', connectionId1, j) ~= 0)
                    data(i, j) = calllib('Thinkgear', 'TG_GetValue', connectionId1, j);
                end
            end
        end
        i = i + 1; % Move to the next row
        
        % Dynamically expand data storage if needed
        if i > size(data, 1)
            data = [data; ones(10000, 14)];  % Expand by 10,000 rows
        end
    end
    pause(1);  % Wait for 1 second before reading the next packet
end

fprintf('Data collection stopped.\n');

% Save data to CSV
csvwrite(path + 'data.csv', data(1:i-1, :));  % Save only collected rows
dlmwrite(path + 'data.csv', data(1:i-1, :), 'precision', '%.6f');

% Disconnect from ThinkGear
calllib('Thinkgear', 'TG_FreeConnection', connectionId1);

% Close the stop button figure
close(fig);

disp('Data saved and connection closed.');
