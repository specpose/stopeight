(* ::Package:: *)

(* ::Input:: *)
(*BeginPackage["Spline`"];*)


(* ::Input:: *)
(*Clear["Spline`*"];*)
(*pascalMatrix::usage="The transpose of a negative Jordan Matrix of dimension";*)


(* ::Input:: *)
(*H1::usage="A linear equation solver taking polynomial coefficients, an affine transformation and two 2D control points";*)
(*H2::usage="A linear equation solver taking polynomial coefficients, an affine transformation and three 2D control points";*)
(*H3::usage="A linear equation solver taking polynomial coefficients, an affine transformation and four 2D control points";*)
(*H4::usage="A linear equation solver taking polynomial coefficients, an affine transformation and five 2D control points";*)
(*arc1::usage="The points of a linear spline with Start and End";*)
(*arc2::usage="The points of a quadratic spline with Start, a bezier control point and End";*)
(*arc3::usage="The points of a quadratic spline with Start, two bezier control points and End";*)
(*arc4::usage="The points of a quadratic spline with Start, three bezier control points and End";*)
(*BC::usage="Used by BS and Pascal";*)
(*Pascal::usage="Returns the coefficients of Pascal's triangle for a binomial of degree";*)
(*BS::usage="Bernstein polynomial?";*)
(*BS2gen::usage="The points of a quadratic polynomial defined by one scalar";*)
(*BS3gen::usage="The points of a cubic polynomial defined by a scalar and a 2D control point";*)
(*BS3gen2::usage="The points of a cubic polynomial defined by two scalars";*)
(*BS4gen::usage="The points of a quartic polynomial defined by a scalar and two 2D control points";*)
(*BS4gen2::usage="The points of a quartic polynomial defined by two scalars and a 2D control point";*)
(*BS4gen3::usage="The points of a quartic polynomial defined by three scalars";*)


(* ::Input:: *)
(*Begin["Spline`Private`"];*)
(**)


(* ::Input:: *)
(*pascalMatrix[n_]:=DiagonalMatrix[Table[1,{n}]]+DiagonalMatrix[Table[-1,{n-1}],-1]*)
(*H1[Coef_,M_,s_,e_]:= Module[{*)
(*MID={{1,1/2}},*)
(*H={{s[[1]],s[[2]]},{e[[1]],e[[2]]}}*)
(*},*)
(*{{s[[1]],s[[2]]},{e[[1]],e[[2]]}}*)
(*]*)
(*H2[Coef_,M_,s_,c1_,e_]:= Module[{*)
(*MID={{1,1/2,(1/2)^2}},*)
(*H={{s[[1]],s[[2]],0},{x,y,0},{e[[1]],e[[2]],0}},dest={{c1[[1]],c1[[2]],0}}*)
(*},*)
(*result = Solve[MID.Coef.M.H==dest,{x,y}];*)
(*{{s[[1]],s[[2]],0},{result[[1]][[1]][[2]],result[[1]][[2]][[2]],0},{e[[1]],e[[2]],0}}*)
(*]*)
(*H3[Coef_,M_,s_,c1_,c2_,e_]:= Module[{*)
(*LEFT={{1,1/3,(1/3)^2,(1/3)^3}},*)
(*RIGHT={{1,2/3,(2/3)^2,(2/3)^3}},*)
(*H={{s[[1]],s[[2]],0,0},{w,x,0,0},{y,z,0,0},{e[[1]],e[[2]],0,0}},*)
(*destL={{c1[[1]],c1[[2]],0,0}},*)
(*destR={{c2[[1]],c2[[2]],0,0}}*)
(*},*)
(*polyL=LEFT.Coef.M.H==destL;*)
(*polyR=RIGHT.Coef.M.H==destR;*)
(*result=Solve[polyL&&polyR,{w,x,y,z}];*)
(*{{s[[1]],s[[2]],0,0},{result[[1]][[1]][[2]],result[[1]][[2]][[2]],0,0},{result[[1]][[3]][[2]],result[[1]][[4]][[2]],0,0},{e[[1]],e[[2]],0,0}}*)
(*]*)
(*H4[Coef_,M_,s_,c1_,c2_,c3_,e_]:= Module[{*)
(*LEFT={{1,1/4,(1/4)^2,(1/4)^3,(1/4)^4}},*)
(*MID={{1,2/4,(2/4)^2,(2/4)^3,(2/4)^4}},*)
(*RIGHT={{1,3/4,(3/4)^2,(3/4)^3,(3/4)^4}},*)
(*H={{s[[1]],s[[2]],0,0,0},{u,v,0,0,0},{w,x,0,0,0},{y,z,0,0,0},{e[[1]],e[[2]],0,0,0}},*)
(*destL={{c1[[1]],c1[[2]],0,0,0}},*)
(*destM={{c2[[1]],c2[[2]],0,0,0}},*)
(*destR={{c3[[1]],c3[[2]],0,0,0}}*)
(*},*)
(*polyL=LEFT.Coef.M.H==destL;*)
(*polyM=MID.Coef.M.H==destM;*)
(*polyR=RIGHT.Coef.M.H==destR;*)
(*result=Solve[polyL&&polyM&&polyR,{u,v,w,x,y,z}];*)
(*{{s[[1]],s[[2]],0,0,0},{result[[1]][[1]][[2]],result[[1]][[2]][[2]],0,0,0},{result[[1]][[3]][[2]],result[[1]][[4]][[2]],0,0,0},{result[[1]][[5]][[2]],result[[1]][[6]][[2]],0,0,0},{e[[1]],e[[2]],0,0,0}}*)
(*]*)
(*arc1[s_,e_]:=Module[{},*)
(*sol = H1[pascalMatrix[2],IdentityMatrix[2],s,e]; Table[{p=Flatten[{{1,t}}.pascalMatrix[2].sol];*)
(*p[[1]],*)
(*p[[2]]*)
(*},{t,0,1,1/2}]*)
(*]*)
(*arc2[s_,c1_,e_]:=Module[{},*)
(*sol = H2[pascalMatrix[3],IdentityMatrix[3],s,c1,e]; Table[{p=Flatten[{{1,t,t^2}}.pascalMatrix[3].sol];*)
(*p[[1]],*)
(*p[[2]]*)
(*},{t,0,1,1/4}]*)
(*]*)
(*arc3[s_,c1_,c2_,e_]:=Module[{},*)
(*sol = H3[pascalMatrix[4],IdentityMatrix[4],s,c1,c2,e]; Table[{p=Flatten[{{1,t,t^2,t^3}}.pascalMatrix[4].sol];*)
(*p[[1]],*)
(*p[[2]]*)
(*},{t,0,1,1/6}]*)
(*]*)
(*arc4[s_,c1_,c2_,c3_,e_]:=Module[{},*)
(*sol = H4[pascalMatrix[5],IdentityMatrix[5],s,c1,c2,c3,e]; Table[{p=Flatten[{{1,t,t^2,t^3,t^4}}.pascalMatrix[5].sol];*)
(*p[[1]],*)
(*p[[2]]*)
(*},{t,0,1,1/8}]*)
(*]*)
(*BC[n_,i_]:=Module[{},Factorial[n]/((Factorial[i])*Factorial[n-i])]*)
(*Pascal[n_]=Module[{},Table[{((-1)^i)*BC[n,i]},{i,0,n}]]*)
(*BS[n_,i_,t_]:=Module[{},BC[n,i]*(t^i)*(1-t)^(n-i)]*)
(*BS2gen[xin_,i_]:=Module[{*)
(*H2*)
(*},*)
(*Clear[y];Clear[x];*)
(*H2={{0,0,0},{x,y,0},{1,0,0}};*)
(*eq=Det[pascalMatrix[3].H2-t*IdentityMatrix[3]]==BS[3,i,t];*)
(*sol=Solve[eq,{y}][[1]][[1]][[2]];*)
(*Table[{p=Flatten[x=xin;y=sol;{{1,t,t^2}}.pascalMatrix[3].H2];*)
(*p[[1]],*)
(*p[[2]]*)
(*},{t,0,1,1/4}]]*)
(*BS3gen[win_,yin_,zin_,i_]:=Module[{*)
(*H3*)
(*},*)
(*Clear[w,x,y,z];*)
(*H3={{0,0,0,0},{w,x,0,0},{y,z,0,0},{1,0,0,0}};*)
(*eq=Det[pascalMatrix[4].H3-t*IdentityMatrix[4]]==BS[4,i,t];*)
(*sol=Solve[eq,{x}][[1]][[1]][[2]];*)
(*Table[{p=Flatten[w=win;x=sol;y=yin;z=zin;{{1,t,t^2,t^3}}.pascalMatrix[4].H3];*)
(*p[[1]],*)
(*p[[2]]*)
(*},{t,0,1,1/6}]]*)
(*BS3gen2[win_,yin_,i_]:=Module[{*)
(*H3,*)
(*H2*)
(*},*)
(*Clear[w,x,y,z];*)
(*H3={{0,0,0,0},{w,x,0,0},{y,z,0,0},{1,0,0,0}};*)
(*eq=Det[pascalMatrix[4].H3-t*IdentityMatrix[4]]==BS[4,i,t];*)
(*sol=Solve[eq,{x}][[1]][[1]][[2]];*)
(*H2={{w,0,0},{y,z,0},{1,0,0}};*)
(*eq2=Det[pascalMatrix[3].H2 -t*IdentityMatrix[3]]==BS[3,i-1,t];*)
(*Clear[w,y,z];*)
(*sol2=Solve[eq2,{z}][[1]][[1]][[2]];*)
(*points=Table[{p=Flatten[w=win;x=sol;y=yin;z=sol2;{{1,t,t^2,t^3}}.pascalMatrix[4].H3];*)
(*p[[1]],*)
(*p[[2]]*)
(*},{t,0,1,1/6}]]*)
(*BS4gen2[uin_,win_,yin_,zin_,i_]:=Module[{*)
(*H4,*)
(*H3*)
(*},*)
(*Clear[u,v,w,x,y,z];*)
(*H4={{0,0,0,0,0},{u,v,0,0,0},{w,x,0,0,0},{y,z,0,0,0},{1,0,0,0,0}};*)
(*eq=Det[pascalMatrix[5].H4-t*IdentityMatrix[5]]==BS[5,i,t];*)
(*sol=Solve[eq,{v}][[1]][[1]][[2]];*)
(*pascalMatrix[4]={{-1,0,0,0},{0,-1,0,0},{0,0,-1,0},{0,0,0,-1}};*)
(*H3={{u,0,0,0},{w,x,0,0},{y,z,0,0},{1,0,0,0}};*)
(*eq2=Det[pascalMatrix[4].H3-t*IdentityMatrix[4]]==BS[4,i-1,t];*)
(*Clear[u,w,x,y,z];*)
(*sol2=Solve[eq2,{x}][[1]][[1]][[2]];*)
(*Table[{p=Flatten[u=uin;v=sol;w=win;x=sol2;y=yin;z=zin;{{1,t,t^2,t^3,t^4}}.pascalMatrix[5].H4];*)
(*p[[1]],*)
(*p[[2]]*)
(*},{t,0,1,1/8}]]*)
(*BS4gen3[uin_,win_,yin_,i_]:=Module[{*)
(*H4,*)
(*H3,*)
(*H2*)
(*},*)
(*Clear[u,v,w,x,y,z];*)
(*H4={{0,0,0,0,0},{u,v,0,0,0},{w,x,0,0,0},{y,z,0,0,0},{1,0,0,0,0}};*)
(*eq=Det[pascalMatrix[5].H4-t*IdentityMatrix[5]]==BS[5,i,t];*)
(*sol=Solve[eq,{v}][[1]][[1]][[2]];*)
(*H3={{u,0,0,0},{w,x,0,0},{y,z,0,0},{1,0,0,0}};*)
(*eq2=Det[pascalMatrix[4].H3-t*IdentityMatrix[4]]==BS[4,i-1,t];*)
(*Clear[u,w,x,y,z];*)
(*sol2=Solve[eq2,{x}][[1]][[1]][[2]];*)
(*H2={{w,0,0},{y,z,0},{1,0,0}};*)
(*eq3=Det[pascalMatrix[3].H2-t*IdentityMatrix[3]]==BS[3,i-2,t];*)
(*sol3=Solve[eq3,{z}][[1]][[1]][[2]];*)
(*Table[{p=Flatten[u=uin;v=sol;w=win;x=sol2;y=yin;z=sol3;{{1,t,t^2,t^3,t^4}}.pascalMatrix[5].H4];*)
(*p[[1]],*)
(*p[[2]]*)
(*},{t,0,1,1/8}]]*)
(*BS4gen[uin_,win_,xin_,yin_,zin_,i_]:=Module[{*)
(*H4*)
(*},*)
(*Clear[u,v,w,x,y,z];*)
(*H4={{0,0,0,0,0},{u,v,0,0,0},{w,x,0,0,0},{y,z,0,0,0},{1,0,0,0,0}};*)
(*eq=Det[pascalMatrix[5].H4-t*IdentityMatrix[5]]==BS[5,i,t];*)
(*sol=Solve[eq,{v}][[1]][[1]][[2]];*)
(*Table[{p=Flatten[u=uin;v=sol;w=win;x=xin;y=yin;z=zin;{{1,t,t^2,t^3,t^4}}.pascalMatrix[5].H4];*)
(*p[[1]],*)
(*p[[2]]*)
(*},{t,0,1,1/8}]]*)


(* ::Input:: *)
(*End[];*)
(*EndPackage[];*)
