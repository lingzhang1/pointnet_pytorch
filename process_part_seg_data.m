% read data
mainpath = 'shapenetcore_partanno_segmentation_benchmark_v0';
path = strcat(mainpath, '/synsetoffset2category.txt');

fileID = fopen(path);
C = textscan(fileID,'%s %s');

for k=1:length(C{2})
    category=C{2}{k};
    data_path = strcat( mainpath, '/', category, '/points', '/*.pts');
    data_files = dir(data_path);
    for n=1:length(files)
        data_path = strcat( mainpath, '/', category, '/points/', data_files(n).name);
        xyzPoints = load(data_path);
        xyzPoints = xyzPoints(:,1:3);

%       cut part of the object
        [Max_v,Max_i] = max(xyzPoints);
        [Min_v,Min_i] = min(xyzPoints);
        Range_value = Max_v - Min_v;
        [value, axis] = max(Range_value);
        A = xyzPoints(:,axis) > (Min_v(axis) + value * 0.3); 
        xyzPoints = xyzPoints(A ~= 0,:);
        
%       get normals
        ptCloud = pointCloud(xyzPoints);
        normals = pcnormals(ptCloud);
        
%       show normals       
        figure;
        pcshow(ptCloud);
        title('Estimated Normals of Point Cloud');
        hold on;

        x = ptCloud.Location(1:1:end,1);
        y = ptCloud.Location(1:1:end,2);
        z = ptCloud.Location(1:1:end,3);
        u = normals(1:1:end,1);
        v = normals(1:1:end,2);
        w = normals(1:1:end,3);

        quiver3(x,y,z,u,v,w);
        hold off
        
%       out put normals and coords
        coords_normal = cat(2, xyzPoints, normals);
        fileID = fopen(data_path, 'w');
        for ii = 1:size(coords_normal,1)
            fprintf(fileID,'%10.8f\t',coords_normal(ii,:));
            fprintf(fileID,'\n');
        end
        fclose(fileID);
    end
end

