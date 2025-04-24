// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

contract Transaction {
    struct User {
        uint256 id;        
        uint256 userid; 
        uint256 amount;
        string status;
        string datevalues;
    }
    
    uint256 private nextId = 1;
    mapping(address => User[]) public userList;

    function addPress(
        uint256 _userid,    
        uint256 _amount,
        string memory _status,
        string memory _datevalues
    ) public {
        uint256 currentId = nextId++;
        userList[msg.sender].push(
            User(currentId, _userid, _amount, _status, _datevalues)
        );
    }

    function getUsers()
        public
        view
        returns (
            uint256[] memory,
            uint256[] memory,
            uint256[] memory,
            string[] memory,
            string[] memory
        )
    {
        uint256 count = userList[msg.sender].length;
        uint256[] memory ids = new uint256[](count);
        uint256[] memory userids = new uint256[](count);
        uint256[] memory amounts = new uint256[](count);
        string[] memory statuses = new string[](count);
        string[] memory dateValues = new string[](count);

        for (uint256 index = 0; index < count; index++) {
            User storage user = userList[msg.sender][index];
            ids[index] = user.id;
            userids[index] = user.userid;
            amounts[index] = user.amount;
            statuses[index] = user.status;
            dateValues[index] = user.datevalues;
        }
        return (ids, userids, amounts, statuses, dateValues);
    }

    
    function updateStatus(uint256 _id, string memory _newStatus) public {
        for (uint i = 0; i < userList[msg.sender].length; i++) {
            if (userList[msg.sender][i].id == _id) {
                userList[msg.sender][i].status = _newStatus;
                break;
            }
        }
    }
}
