tunnel:
	ssh -L 8080:127.0.0.1:8080 xilinx@makerslab-fpga-26.d2.comp.nus.edu.sg

protoc:
	rm -f pb/*.py
	python3 -m grpc_tools.protoc -Iproto --python_out=external_communication/pb --pyi_out=external_communication/pb --grpc_python_out=external_communication/pb proto/*.proto

run:
	python3 main.py

test_ai:
	su - root -c "python3 /home/xilinx/external_comms/test_ai.py"