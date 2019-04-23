# How to run?

​	Dependencies : <br>		numpy, <br>		pytorch1.0.1.post2 (The newest edition download from <https://pytorch.org/> )<br>		cuda10.0<br>		CUDA 10.0.130<br>		CUDNN 7.5.0.56	

​	In the root directory, there are two source files : board.py and reversi.py, which are offered by the origin engine frame.<br>And a single directory : engines. You can get my engine interface "unispac_21.py" in the "engines" directory.<br>	Run the engine by input :<br>		python3 reversi.py -a eona -b unispac_21<br>	Then you can see the match play between my engine and the example engine.<br>	Note that in oder to take best use of the time resource, each step will cost about 30 seconds.. <br>	If you want to see the result more quickly, open the source file : "unispac_21.py" and modify the args.simCntOfMCT.<br>	100~500 is recommended..

​	!!! Last but not least..<br>	If you want to transplant my engine to another game environment. Don't forget to take along the directory "alpha" under "engines" togther.<br>	The directory "alpha" offers the key module of my engine..<br>	And as there may be a problem of path.. It is recommended to organize the game just like the example frame.. Put all the engine files in the engiles directory.<br>Put my "alpha" directory under the engiens dir.. And the reversi.py is under the root directory..	



# About author

​	Developer : Qi Xiangyu(漆翔宇)<br>	Major : Computer Science and Technology<br>	Tel : 17342017090<br>	Email : unispac@zju.edu.cn<br>	QQ : 416162623<br>	

​	Please contact with me if you have encountered any problems when running it..	

​	
