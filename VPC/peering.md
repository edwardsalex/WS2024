## Step 1: Create Peering Connection
![Step 1](peering-step1.png)
Click on ```Create peering connection``` in order to start the wizard.

![Step 2, Part 1](peering-step2-part1.png)
![Step 2, Part 2](peering-step2-part2.png)

Fill out the wizard like shown above, and then accept the peering connection as soon as the wizard is complete.

![Step 2, Part 3](peering-step2-part3.png)

## Step 2: Fix routes to allow for VPC-VPC communication
For each VPC, change their route tables (pub, or private, depending on the needs and requirements) as shown below.

```VPC A```:
![VPC-A](step3-part1.png)
```VPC B```
![VPC-B](step3-part2.png)

## Step 3: Ensure that Security Groups allow Traffic
Depending on the service, add the ports, and the CIDR block that is peering with the incoming VPC that has the service available, like shown:
![Funny](step4-part1.png)

Once complete, you should be able to peer with VPC.