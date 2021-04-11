-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2021-04-11 15:51:09
-- 伺服器版本： 10.4.17-MariaDB
-- PHP 版本： 8.0.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `food_delivery`
--

-- --------------------------------------------------------

--
-- 資料表結構 `cuisines`
--

CREATE TABLE `cuisines` (
  `type` varchar(50) DEFAULT NULL,
  `restaurant` varchar(100) DEFAULT NULL,
  `item` varchar(100) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `img` blob DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 傾印資料表的資料 `cuisines`
--

INSERT INTO `cuisines` (`type`, `restaurant`, `item`, `price`, `img`) VALUES
('Western Food', 'Outback Steakhouse', 'Alice Springs Chicken', 98, 0x616c6963655f737072696e67735f322e6a7067),
('Western Food', 'Outback Steakhouse', 'Spring Chicken with mashed potato', 88, 0x737072696e675f636869636b656e5f312e6a7067),
('Singapore Hainanese Chicken', 'Asam Chicken Rice', 'Hainanese Chicken Rice', 88, 0x6861696e616e6573655f312e6a7067),
('Japanese Sushi', 'Genki Sushi', 'Sushi Set (8 in total)', 40, 0x73757368695f7365742e6a7067),
('Japanese Sushi', 'Genki Sushi', 'Beef Udon', 34, 0x626565665f75646f6e2e6a7067),
('Singapore Hainanese Chicken', 'Asam Chicken Rice', 'Bak Kut Teh', 94, 0x62616b2e6a7067);

-- --------------------------------------------------------

--
-- 資料表結構 `customers`
--

CREATE TABLE `customers` (
  `no` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `tel` int(11) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `member` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 傾印資料表的資料 `customers`
--

INSERT INTO `customers` (`no`, `name`, `username`, `password`, `tel`, `email`, `member`) VALUES
(1, 'Dominic', 'dominsham807', 'Ds996322', 90918589, 'dominicsham2000@gmail.com', 1);

-- --------------------------------------------------------

--
-- 資料表結構 `order_receipts`
--

CREATE TABLE `order_receipts` (
  `name` varchar(50) NOT NULL,
  `order_no` int(11) DEFAULT NULL,
  `items` varchar(350) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `price` decimal(5,1) DEFAULT NULL,
  `discount` decimal(5,2) DEFAULT NULL,
  `payment_method` varchar(50) DEFAULT NULL,
  `delivery_time` time DEFAULT NULL,
  `delivery_addr` varchar(200) DEFAULT NULL,
  `member` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 傾印資料表的資料 `order_receipts`
--

INSERT INTO `order_receipts` (`name`, `order_no`, `items`, `quantity`, `price`, `discount`, `payment_method`, `delivery_time`, `delivery_addr`, `member`) VALUES
('Dominic Sham', 126, 'Alice Springs Chicken*2, Hainanese Chicken Rice*2, Beef Udon*1', 5, '324.8', '0.80', 'Octopus', '19:45:00', 'T3, 57/F, B-C, Ocean Pointe, Sham Tseng', 1),
('Dominic', 238, 'Alice Springs Chicken*1, Hainanese Chicken Rice*2, Sushi Set (8 in total)*1, Beef Udon*1', 5, '278.4', '0.80', 'Octopus', '19:00:00', 'T3, 57/F, B-C, Ocean Pointe, Sham Tseng', 1);

-- --------------------------------------------------------

--
-- 資料表結構 `restaurants`
--

CREATE TABLE `restaurants` (
  `type` varchar(100) DEFAULT NULL,
  `restaurant` varchar(60) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `open_time` time DEFAULT NULL,
  `close_time` time DEFAULT NULL,
  `tel` int(11) DEFAULT NULL,
  `hotline` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 傾印資料表的資料 `restaurants`
--

INSERT INTO `restaurants` (`type`, `restaurant`, `address`, `open_time`, `close_time`, `tel`, `hotline`) VALUES
('Singapore Hainanese Chicken', 'Asam Chicken Rice', 'L2-28, Festival Walk, Tat Chee Avenue, Kowloon Tong', '11:00:00', '22:00:00', 22610989, 30551274),
('Singapore Hainanese Chicken', 'Hawker 18', 'Shop 410, Metroplaza, Kwai Fong', '11:00:00', '21:00:00', 29541546, 33547845),
('Western Food', 'Outback Steakhouse', '7/F, Chinachem Plaza, Tsim Sha Tsui, Kowloon', '12:00:00', '22:00:00', 24931874, 34457841),
('Japanese Sushi', 'Genki Sushi', 'B105-B108, Tsuen Wan Plaza, Tsuen Wan, New Territories', '11:30:00', '22:00:00', 24988754, 31665482),
('Singapore Hainanese Chicken', 'ABC Restaurant', 'Sham Tsz Street 8', '13:00:00', '22:00:00', 24551232, 30887454);

-- --------------------------------------------------------

--
-- 資料表結構 `staff`
--

CREATE TABLE `staff` (
  `no` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `staff_id` int(11) DEFAULT NULL,
  `tel` int(11) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `duty` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 傾印資料表的資料 `staff`
--

INSERT INTO `staff` (`no`, `name`, `username`, `password`, `staff_id`, `tel`, `email`, `duty`) VALUES
(1, 'Michael', 'mchwong109', 'MW552478', 56237772, 63000882, 'mchwong109@gmail.com', 'Western Food'),
(2, 'Jason', 'jcho509', 'JC522130', 52418895, 54099254, 'jcho509@gmail.com', 'Singapore Hainanese Chicken'),
(3, 'Jessica', 'jyuen614', 'JY996322', 51244156, 96540872, 'jyuen614@gmail.com', 'Japanese Sushi');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`no`);

--
-- 資料表索引 `staff`
--
ALTER TABLE `staff`
  ADD PRIMARY KEY (`no`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `customers`
--
ALTER TABLE `customers`
  MODIFY `no` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `staff`
--
ALTER TABLE `staff`
  MODIFY `no` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
