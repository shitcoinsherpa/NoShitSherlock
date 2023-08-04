// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract RiskGame {
    ERC20 public nssToken;
    uint256 public constant MAX_INT = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;
    uint256 public contractBalance;
    
    struct GameDetails {
        uint256 lastGenerationBlock;
        uint256 lastWinBlock;
        uint256 attackAmount;
        uint256 attackFromTerritory;
        uint256 attackToTerritory;
        uint256 attackPrevrandao;
        uint256 currentWoundedSoldiers;
        uint256 lastDayWoundedSoldiers;
        uint256 deadSoldiers;
        uint256 lastRewardDistribution;
        uint256 lastRewardBlock;
        bool gameNotInitialized;
        bool gameOver;
        address attacker;
    }

    GameDetails public gameDetails;

    struct GameSettings {
        uint256 blocksPerDay;
        address deadSoldiersAddress;
    }

    GameSettings public gameSettings;

    struct PlayerDetails {
        uint256 soldiers;
        uint256 ownerTerritoryCount;
        uint256 initialClaims;
        uint256 maxInitialClaims;
        uint256 DailyRewards;
        uint256 EndGameReward;
        bool insurrectionMap;
    }

    mapping(address => PlayerDetails) public playerDetails;

    struct Territory {
        uint256 soldiers;
        address owner;
    }

    struct Continent {
        uint256[] territories;
        uint256 soldierBonus;
    }

    Continent[] public continents;

    mapping(uint256 => Territory) public territories;
    mapping(uint256 => uint256[]) public adjacencyMap;

    event Insurrection(
        address indexed insurrectionist,
        uint256 indexed territory,
        uint256 tokens,
        bool successful
    );

    event BattleResult(
        address indexed attacker,
        uint256 fromTerritory,
        address indexed defender,
        uint256 toTerritory,
        uint256 attackerKilled,
        uint256 attackerWounded,
        uint256 defenderKilled,
        uint256 defenderWounded
    );

    event Attack(
        address indexed attacker,
        uint256 indexed fromTerritory,
        uint256 indexed toTerritory,
        uint256 amount
    );

    event TerritoryOwnerChange(
        uint256 indexed territory,
        address indexed previousOwner,
        address indexed newOwner
    );

    event PlaceSoldiers(
        address indexed player,
        uint256 indexed territory,
        uint256 amount
    );

    constructor() {
        for (uint256 i = 0; i < 42; i++) {
            territories[i].owner = address(0);
            territories[i].soldiers = 0;
            playerDetails[address(0)].maxInitialClaims = 4;
        }
        gameDetails.gameOver = false;
        gameDetails.lastRewardBlock = block.number;
        gameSettings.deadSoldiersAddress = 0xA07f15D9c6aFD0f846606A635E0a39e0a5235BDc;
        nssToken = ERC20(0x2Ce9bD8Eb5829A5781cFC6c0388C87151B9DB3d2); // NSS token

        continents.push(Continent(new uint256[](9), 5));  // North America
        continents[0].territories = [0, 1, 2, 3, 4, 5, 6, 7, 8];
    
        continents.push(Continent(new uint256[](4), 2));  // South America
        continents[1].territories = [9, 10, 11, 12];
    
        continents.push(Continent(new uint256[](6), 3));  // Africa
        continents[2].territories = [13, 14, 15, 16, 17, 18];

        continents.push(Continent(new uint256[](7), 5));  // Europe
        continents[3].territories = [19, 20, 21, 22, 23, 24, 25];
    
        continents.push(Continent(new uint256[](12), 7)); // Asia
        continents[4].territories = [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37];

        continents.push(Continent(new uint256[](4), 2));  // Australia
        continents[5].territories = [38, 39, 40, 41];

        initAdjacencyMap();
    }

    function initAdjacencyMap() internal {
        // North America
        adjacencyMap[0] = [1, 2, 5, 35];  // Alaska
        adjacencyMap[1] = [0, 2, 5, 6];  // Northwest Territory
        adjacencyMap[2] = [0, 1, 3, 6]; // Alberta
        adjacencyMap[3] = [2, 4, 9]; // Central America
        adjacencyMap[4] = [3, 6, 7]; // Eastern United States
        adjacencyMap[5] = [0, 1, 6, 19]; // Greenland
        adjacencyMap[6] = [1, 2, 4, 5, 7, 8]; // Ontario
        adjacencyMap[7] = [4, 6, 8]; // Quebec
        adjacencyMap[8] = [2, 6, 7]; // Western United States

        // South America
        adjacencyMap[9] = [3, 10, 12]; // Venezuela
        adjacencyMap[10] = [9, 11, 12]; // Peru
        adjacencyMap[11] = [10, 12]; // Argentina
        adjacencyMap[12] = [9, 10, 11, 13]; // Brazil

        // Africa
        adjacencyMap[13] = [12, 14, 15, 16]; // North Africa
        adjacencyMap[14] = [13, 15, 19, 24]; // Egypt
        adjacencyMap[15] = [13, 14, 16, 17, 18, 26]; // East Africa
        adjacencyMap[16] = [13, 15, 17]; // Congo
        adjacencyMap[17] = [15, 16, 18]; // South Africa
        adjacencyMap[18] = [15, 17]; // Madagascar

        // Europe
        adjacencyMap[19] = [5, 20, 25]; // Iceland
        adjacencyMap[20] = [19, 21, 22, 25]; // Scandinavia
        adjacencyMap[21] = [20, 22, 23, 26]; // Ukraine
        adjacencyMap[22] = [20, 21, 23, 24]; // Northern Europe
        adjacencyMap[23] = [22, 24, 25]; // Western Europe
        adjacencyMap[24] = [14, 22, 23, 26]; // Southern Europe
        adjacencyMap[25] = [19, 20, 23]; // Great Britain

        // Asia
        adjacencyMap[26] = [21, 24, 27, 28, 15]; // Middle East
        adjacencyMap[27] = [26, 28, 32]; // Afghanistan
        adjacencyMap[28] = [26, 27, 29, 30]; // India
        adjacencyMap[29] = [28, 30, 38]; // Siam
        adjacencyMap[30] = [28, 29, 31]; // China
        adjacencyMap[31] = [30, 32, 33, 34, 35]; // Mongolia
        adjacencyMap[32] = [27, 31, 33]; // Ural
        adjacencyMap[33] = [31, 32, 34, 35]; // Siberia
        adjacencyMap[34] = [31, 33, 35]; // Irkutsk
        adjacencyMap[35] = [0, 31, 34, 36]; // Yakutsk
        adjacencyMap[36] = [35, 37]; // Kamchatka

        // Australia
        adjacencyMap[37] = [36, 38, 39, 41]; // Indonesia
        adjacencyMap[38] = [37, 39]; // New Guinea
        adjacencyMap[39] = [37, 38, 40]; // Eastern Australia
        adjacencyMap[40] = [37, 39, 41]; // Western Australia
        adjacencyMap[41] = [37, 40]; // New Zealand
    }

    function checkGameOver() internal view returns (bool) {
        address potentialWinner = territories[0].owner;

        for (uint i = 1; i < 42; i++) {
            if (territories[i].owner != potentialWinner) {
                return false;
            }
        }

        return true;
    }

    function buySoldier(uint256 amount) external {
        require(nssToken.allowance(msg.sender, address(this)) >= amount, "Allowance too low");
        playerDetails[msg.sender].soldiers += amount;
        if (playerDetails[msg.sender].maxInitialClaims == 0) {
            playerDetails[msg.sender].maxInitialClaims = 4;
        }
        bool transferSuccess = nssToken.transferFrom(msg.sender, address(this), amount);
        require(transferSuccess, "NSS transfer failed");
    }

    function battleResult(uint256 attackerWounded, uint256 defenderWounded,
                          uint256 attackerKilled, uint256 defenderKilled) internal {
        gameDetails.currentWoundedSoldiers += attackerWounded + defenderWounded;
        gameDetails.deadSoldiers += attackerKilled + defenderKilled;
    }

    function distributeRewards() public {
        if (block.number - gameDetails.lastRewardBlock >= 5760) {
            gameDetails.lastDayWoundedSoldiers = gameDetails.currentWoundedSoldiers;
            gameDetails.currentWoundedSoldiers = 0;
            uint256 totalRewards = gameDetails.lastDayWoundedSoldiers * 80 / 100;
            for (uint i = 0; i < continents.length; i++) {
                address owner = territories[continents[i].territories[0]].owner;
                bool singleOwner = true;

                for (uint j = 1; j < continents[i].territories.length; j++) {
                    if (territories[continents[i].territories[j]].owner != owner) {
                        singleOwner = false;
                        break;
                    }
                }

                if (singleOwner && owner != address(0)) {
                    uint256 reward = (totalRewards * continents[i].soldierBonus * 80 / 100) / continents[i].territories.length;
                    playerDetails[owner].DailyRewards += reward;
                    totalRewards -= reward * continents[i].territories.length;
                }
            }

            gameDetails.lastDayWoundedSoldiers = (totalRewards * 20) / 100;
            gameDetails.deadSoldiers = 0;
            gameDetails.lastRewardBlock = block.number;
        }
    }

    function checkDailyRewards() public returns (uint256) {
        distributeRewards();
        return playerDetails[msg.sender].DailyRewards;
    }

    function claimDailyRewards() public {
        playerDetails[msg.sender].soldiers += playerDetails[msg.sender].DailyRewards;
        playerDetails[msg.sender].DailyRewards = 0;
    }

    function placeSoldiers(uint256 territory, uint256 amount) external {
        require(!gameDetails.gameOver, "Game is over");
        require(playerDetails[msg.sender].soldiers >= amount, "You do not have enough soldiers");

        if (territories[territory].owner == address(0)) {
            require(playerDetails[msg.sender].initialClaims < playerDetails[msg.sender].maxInitialClaims, "You have already claimed 4 territories");
            territories[territory].owner = msg.sender;
            playerDetails[msg.sender].initialClaims += 1;
            playerDetails[msg.sender].ownerTerritoryCount += 1;
        } else {
            require(territories[territory].owner == msg.sender, "You do not own this territory");
        }

        playerDetails[msg.sender].soldiers -= amount;
        territories[territory].soldiers += amount;

        emit PlaceSoldiers(msg.sender, territory, amount);
    }

    function insurrection(uint256 territory, uint256 tokens) external {
        require(!gameDetails.gameOver, "Game is over");
        require(playerDetails[msg.sender].ownerTerritoryCount == 0, "Player is currently holding territories");
        require(tokens >= 1000, "Minimum of 1000 NSS tokens required for insurrection");
        require(playerDetails[msg.sender].soldiers >= tokens || territories[territory].soldiers == 1, "Not enough soldiers for insurrection");
        require(!playerDetails[msg.sender].insurrectionMap, "Player has already initiated an insurrection");
        require(territories[territory].owner != msg.sender, "Cannot initiate insurrection on your own territory");

        uint256 attackerStrength = getRand(gameDetails.attackPrevrandao) % tokens;
        uint256 defenderStrength = getRand(uint256(keccak256(abi.encodePacked(territories[territory].owner)))) % territories[territory].soldiers;

        uint256 attackerKilled = (attackerStrength * 269) / 10000;
        uint256 defenderKilled = (defenderStrength * 269) / 10000;

        playerDetails[msg.sender].soldiers -= attackerKilled;
        territories[territory].soldiers -= defenderKilled;

        uint256 attackerWounded = attackerKilled < tokens ? (defenderStrength * (tokens - attackerKilled)) / (attackerStrength + defenderStrength) : 0;
        uint256 defenderWounded = defenderKilled < territories[territory].soldiers ? (attackerStrength * (territories[territory].soldiers - defenderKilled)) / (attackerStrength + defenderStrength) : 0;

        playerDetails[msg.sender].soldiers -= attackerWounded;
        territories[territory].soldiers -= defenderWounded;

        battleResult(attackerWounded, defenderWounded, attackerKilled, defenderKilled);

        if (attackerStrength > defenderStrength && defenderKilled + defenderWounded >= territories[territory].soldiers) {
            address previousOwner = territories[territory].owner;
            territories[territory].owner = msg.sender;
            territories[territory].soldiers = tokens - attackerKilled - attackerWounded;
            playerDetails[previousOwner].ownerTerritoryCount--;
            playerDetails[msg.sender].ownerTerritoryCount++;
            playerDetails[msg.sender].insurrectionMap = true;
        }

        bool transferSuccess = nssToken.transfer(gameSettings.deadSoldiersAddress, attackerKilled + defenderKilled);
        require(transferSuccess, "NSS transfer failed");

        gameDetails.attackFromTerritory = 43;

        emit BattleResult(msg.sender, gameDetails.attackFromTerritory, territories[territory].owner, territory, attackerKilled, attackerWounded, defenderKilled, defenderWounded);
        emit Insurrection(msg.sender, territory, tokens, territories[territory].owner == msg.sender);

        if (allTerritoriesOwnedBy(msg.sender) && territories[43].owner == address(0)) {
            gameDetails.gameOver = true;
            gameDetails.lastWinBlock = block.number;
        }
    }

    function attack(uint256 fromTerritory, uint256 toTerritory, uint256 amount) external {
        require(!gameDetails.gameOver, "Game is over");
        require(territories[fromTerritory].owner == msg.sender, "You do not own this territory");
        require(amount < territories[fromTerritory].soldiers || territories[toTerritory].soldiers == 1, "Not enough soldiers to attack");
        require(isAdjacent(fromTerritory, toTerritory), "Territories are not adjacent");

        uint256 attackerStrength = getRand(gameDetails.attackPrevrandao) % amount;
        uint256 defenderStrength = getRand(uint256(keccak256(abi.encodePacked(territories[toTerritory].owner)))) % territories[toTerritory].soldiers;

        uint256 attackerKilled = (attackerStrength * 269) / 10000;
        uint256 defenderKilled = (defenderStrength * 269) / 10000;

        require(attackerKilled <= amount, "All attacker soldiers were killed");
        require(defenderKilled <= territories[toTerritory].soldiers, "All defender soldiers were killed");

        territories[fromTerritory].soldiers -= attackerKilled;
    
        uint256 soldierCountBeforeAttack = territories[toTerritory].soldiers;
        territories[toTerritory].soldiers -= defenderKilled;

        uint256 attackerWounded = 0;
        uint256 defenderWounded = 0;

        if (attackerKilled < amount) {
            attackerWounded = (defenderStrength * (amount - attackerKilled)) / (attackerStrength + defenderStrength);
        }

        if (defenderKilled < soldierCountBeforeAttack) {
            defenderWounded = (attackerStrength * (soldierCountBeforeAttack - defenderKilled)) / (attackerStrength + defenderStrength);
        }

        require(attackerWounded <= territories[fromTerritory].soldiers, "More attacker soldiers were wounded than available");
        require(defenderWounded <= soldierCountBeforeAttack, "More defender soldiers were wounded than available");

        territories[fromTerritory].soldiers -= attackerWounded;
        territories[toTerritory].soldiers -= defenderWounded;

        battleResult(attackerWounded, defenderWounded, attackerKilled, defenderKilled);

        if (territories[toTerritory].soldiers <= 0) {
            address previousOwner = territories[toTerritory].owner;
            territories[toTerritory].owner = msg.sender;
            playerDetails[previousOwner].ownerTerritoryCount--;
            playerDetails[msg.sender].ownerTerritoryCount++;
            territories[toTerritory].soldiers = amount / 2;
            territories[fromTerritory].soldiers -= amount / 2;
            emit TerritoryOwnerChange(toTerritory, previousOwner, msg.sender);
        }

        if (allTerritoriesOwnedBy(msg.sender)){
            gameDetails.gameOver = true;
            gameDetails.lastWinBlock = block.number;
        }

        emit BattleResult(msg.sender, fromTerritory, territories[toTerritory].owner, toTerritory, attackerKilled, attackerWounded, defenderKilled, defenderWounded);
        emit Attack(msg.sender, fromTerritory, toTerritory, amount);
    }

    function isAdjacent(uint256 fromTerritory, uint256 toTerritory) internal view returns (bool) {
        uint256[] memory adjacentTerritories = adjacencyMap[fromTerritory];

        for (uint i = 0; i < adjacentTerritories.length; i++) {
            if (adjacentTerritories[i] == toTerritory) {
                return true;
            }
        }

        return false;
    }

    function getRand(uint256 salt) internal view returns (uint256) {
        return uint256(keccak256(abi.encodePacked(blockhash(block.number - 1), salt)));
    }

    function allTerritoriesOwnedBy(address owner) public view returns (bool) {
        for (uint i = 0; i < 42; i++) {
            if (territories[i].owner != owner) {
                return false;
            }
        }
        return true;
    }

    function claimEndGameRewards() external {
        require(gameDetails.gameOver, "Game is not over");
    
        uint256 reward = nssToken.balanceOf(address(this));
        uint256 winnerReward = (reward * 9310) / 10000;
        contractBalance = reward - winnerReward;

        require(allTerritoriesOwnedBy(msg.sender), "Only winner can claim the reward");
        bool transferSuccess = nssToken.transfer(msg.sender, winnerReward);
        require(transferSuccess, "NSS transfer failed");

        resetGame();
        emit GameEnded(msg.sender, winnerReward);
    }

    function endGame() external {
        require(block.number > gameDetails.lastWinBlock + 2 * gameSettings.blocksPerDay, "Game has not yet ended");
        resetGame();
        emit GameEnded(address(0), 0);
    }

    function resetGame() internal {
        gameDetails.gameOver = true;
        for (uint256 i = 0; i < 42; i++) {
            territories[i].owner = address(0);
            territories[i].soldiers = 0;
            playerDetails[address(0)].ownerTerritoryCount = 0;
            playerDetails[msg.sender].initialClaims = 0;
        }
        gameDetails.gameOver = false;
    }

    event GameEnded(address winner, uint256 reward);
    }
