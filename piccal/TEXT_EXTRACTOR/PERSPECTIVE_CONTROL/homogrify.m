function [ corrected_image ] = homogrify( img, X, Y )
%HOMOGRIFY Summary of this function goes here
%   Detailed explanation goes here


% This line fucks up our corners
%[X, Y] = sortPolyFromClockwiseStartingFromTopLeft( X, Y );


%x=[1;210;210;1];
%y=[1;1;297;297];
[height, width, depth] = size(img);

% x=[1;width;width;1];
% y=[1;1;height;height];
% 
% % c)
% A=zeros(8,8);
% A(1,:)=[X(1),Y(1),1,0,0,0,-1*X(1)*x(1),-1*Y(1)*x(1)];
% A(2,:)=[0,0,0,X(1),Y(1),1,-1*X(1)*y(1),-1*Y(1)*y(1)];
% 
% A(3,:)=[X(2),Y(2),1,0,0,0,-1*X(2)*x(2),-1*Y(2)*x(2)];
% A(4,:)=[0,0,0,X(2),Y(2),1,-1*X(2)*y(2),-1*Y(2)*y(2)];
% 
% A(5,:)=[X(3),Y(3),1,0,0,0,-1*X(3)*x(3),-1*Y(3)*x(3)];
% A(6,:)=[0,0,0,X(3),Y(3),1,-1*X(3)*y(3),-1*Y(3)*y(3)];
% 
% A(7,:)=[X(4),Y(4),1,0,0,0,-1*X(4)*x(4),-1*Y(4)*x(4)];
% A(8,:)=[0,0,0,X(4),Y(4),1,-1*X(4)*y(4),-1*Y(4)*y(4)];
% 
% v=[x(1);y(1);x(2);y(2);x(3);y(3);x(4);y(4)];
% 
% u=A\v;
% %which reshape
% 
% U=reshape([u;1],3,3)';

% H = FitHomography([X(1) Y(1);X(2) Y(2);X(3) Y(3);X(4) Y(4)],[1 1;width 1;width height;1 height])
H = homography_solve([X(1) Y(1);X(2) Y(2);X(3) Y(3);X(4) Y(4)]',[1 1;width 1;width height;1 height]');

% w=U*[X';Y';ones(1,4)];
% w=w./(ones(3,1)*w(3,:));

% d)
%which maketform
T=maketform('projective',H');

%which imtransform
corrected_image =imtransform(img,T,'XData',[1 width],'YData',[1 height]);
%corrected_image = img;
%imshow(corrected_image);
imwrite(corrected_image, '/home/ubuntu/matlab_homogrified.jpg');
end

