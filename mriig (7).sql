-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 18, 2026 at 12:08 PM
-- Server version: 11.8.3-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mriig`
--

-- --------------------------------------------------------

--
-- Table structure for table `api_emailotp`
--

CREATE TABLE `api_emailotp` (
  `id` bigint(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  `otp` varchar(6) NOT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add category', 7, 'add_category'),
(26, 'Can change category', 7, 'change_category'),
(27, 'Can delete category', 7, 'delete_category'),
(28, 'Can view category', 7, 'view_category'),
(29, 'Can add order', 8, 'add_order'),
(30, 'Can change order', 8, 'change_order'),
(31, 'Can delete order', 8, 'delete_order'),
(32, 'Can view order', 8, 'view_order'),
(33, 'Can add product', 9, 'add_product'),
(34, 'Can change product', 9, 'change_product'),
(35, 'Can delete product', 9, 'delete_product'),
(36, 'Can view product', 9, 'view_product'),
(37, 'Can add order item', 10, 'add_orderitem'),
(38, 'Can change order item', 10, 'change_orderitem'),
(39, 'Can delete order item', 10, 'delete_orderitem'),
(40, 'Can view order item', 10, 'view_orderitem'),
(41, 'Can add product image', 11, 'add_productimage'),
(42, 'Can change product image', 11, 'change_productimage'),
(43, 'Can delete product image', 11, 'delete_productimage'),
(44, 'Can view product image', 11, 'view_productimage'),
(45, 'Can add product variation', 12, 'add_productvariation'),
(46, 'Can change product variation', 12, 'change_productvariation'),
(47, 'Can delete product variation', 12, 'delete_productvariation'),
(48, 'Can view product variation', 12, 'view_productvariation'),
(49, 'Can add product detail section', 13, 'add_productdetailsection'),
(50, 'Can change product detail section', 13, 'change_productdetailsection'),
(51, 'Can delete product detail section', 13, 'delete_productdetailsection'),
(52, 'Can view product detail section', 13, 'view_productdetailsection'),
(53, 'Can add user', 14, 'add_customuser'),
(54, 'Can change user', 14, 'change_customuser'),
(55, 'Can delete user', 14, 'delete_customuser'),
(56, 'Can view user', 14, 'view_customuser'),
(57, 'Can add contact message', 15, 'add_contactmessage'),
(58, 'Can change contact message', 15, 'change_contactmessage'),
(59, 'Can delete contact message', 15, 'delete_contactmessage'),
(60, 'Can view contact message', 15, 'view_contactmessage'),
(61, 'Can add brand', 16, 'add_brand'),
(62, 'Can change brand', 16, 'change_brand'),
(63, 'Can delete brand', 16, 'delete_brand'),
(64, 'Can view brand', 16, 'view_brand'),
(65, 'Can add Blog Post', 17, 'add_blog'),
(66, 'Can change Blog Post', 17, 'change_blog'),
(67, 'Can delete Blog Post', 17, 'delete_blog'),
(68, 'Can view Blog Post', 17, 'view_blog'),
(69, 'Can add Content Management System', 18, 'add_cms'),
(70, 'Can change Content Management System', 18, 'change_cms'),
(71, 'Can delete Content Management System', 18, 'delete_cms'),
(72, 'Can view Content Management System', 18, 'view_cms'),
(73, 'Can add Profile Setting', 19, 'add_profile_setting'),
(74, 'Can change Profile Setting', 19, 'change_profile_setting'),
(75, 'Can delete Profile Setting', 19, 'delete_profile_setting'),
(76, 'Can view Profile Setting', 19, 'view_profile_setting'),
(77, 'Can add slider', 20, 'add_slider'),
(78, 'Can change slider', 20, 'change_slider'),
(79, 'Can delete slider', 20, 'delete_slider'),
(80, 'Can view slider', 20, 'view_slider'),
(81, 'Can add Blog Category', 21, 'add_blogcategory'),
(82, 'Can change Blog Category', 21, 'change_blogcategory'),
(83, 'Can delete Blog Category', 21, 'delete_blogcategory'),
(84, 'Can view Blog Category', 21, 'view_blogcategory'),
(85, 'Can add sub category', 22, 'add_subcategory'),
(86, 'Can change sub category', 22, 'change_subcategory'),
(87, 'Can delete sub category', 22, 'delete_subcategory'),
(88, 'Can view sub category', 22, 'view_subcategory'),
(89, 'Can add user address', 23, 'add_useraddress'),
(90, 'Can change user address', 23, 'change_useraddress'),
(91, 'Can delete user address', 23, 'delete_useraddress'),
(92, 'Can view user address', 23, 'view_useraddress'),
(93, 'Can add email otp', 24, 'add_emailotp'),
(94, 'Can change email otp', 24, 'change_emailotp'),
(95, 'Can delete email otp', 24, 'delete_emailotp'),
(96, 'Can view email otp', 24, 'view_emailotp'),
(97, 'Can add Coupon', 25, 'add_coupon'),
(98, 'Can change Coupon', 25, 'change_coupon'),
(99, 'Can delete Coupon', 25, 'delete_coupon'),
(100, 'Can view Coupon', 25, 'view_coupon'),
(101, 'Can add Coupon Usage', 26, 'add_couponusage'),
(102, 'Can change Coupon Usage', 26, 'change_couponusage'),
(103, 'Can delete Coupon Usage', 26, 'delete_couponusage'),
(104, 'Can view Coupon Usage', 26, 'view_couponusage'),
(105, 'Can add payment', 27, 'add_payment'),
(106, 'Can change payment', 27, 'change_payment'),
(107, 'Can delete payment', 27, 'delete_payment'),
(108, 'Can view payment', 27, 'view_payment'),
(109, 'Can add offer', 28, 'add_offer'),
(110, 'Can change offer', 28, 'change_offer'),
(111, 'Can delete offer', 28, 'delete_offer'),
(112, 'Can view offer', 28, 'view_offer'),
(113, 'Can add Offer Product', 29, 'add_offerproduct'),
(114, 'Can change Offer Product', 29, 'change_offerproduct'),
(115, 'Can delete Offer Product', 29, 'delete_offerproduct'),
(116, 'Can view Offer Product', 29, 'view_offerproduct');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$1000000$zWQAV4KzRIxEuij9MZeCt3$s1c1PlAv/PAJXPEx4YFns+7kXxVC9/S6BeEnXsnohyw=', '2025-12-20 16:50:29.961438', 1, 'mriiggadmin', 'Mriigg', 'ecom', '', 1, 1, '2025-10-15 19:36:00.000000');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cms_blog`
--

CREATE TABLE `cms_blog` (
  `id` bigint(20) NOT NULL,
  `title` varchar(200) NOT NULL,
  `slug` varchar(200) DEFAULT NULL,
  `short_description` varchar(300) DEFAULT NULL,
  `content` longtext DEFAULT NULL,
  `featured_image` varchar(100) DEFAULT NULL,
  `post_date` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `view_counter` int(11) NOT NULL,
  `order` int(11) DEFAULT NULL,
  `status` varchar(10) NOT NULL,
  `is_featured` tinyint(1) NOT NULL,
  `meta_title` varchar(200) DEFAULT NULL,
  `meta_description` longtext DEFAULT NULL,
  `author_id` int(11) NOT NULL,
  `category_id` bigint(20) DEFAULT NULL,
  `subcategory_id` bigint(20) DEFAULT NULL,
  `tags` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cms_blog`
--

INSERT INTO `cms_blog` (`id`, `title`, `slug`, `short_description`, `content`, `featured_image`, `post_date`, `updated_at`, `view_counter`, `order`, `status`, `is_featured`, `meta_title`, `meta_description`, `author_id`, `category_id`, `subcategory_id`, `tags`) VALUES
(1, 'Cosmetics Matte to Last Pore Blurring Loose Powder Banana', 'cosmetics-matte-to-last-pore-blurring-loose-powder-banana', 'Cosmetics Matte to Last Pore Blurring Loose Powder Banana', '<h2>Cosmetics Matte to Last Pore Blurring Loose Powder Banana 03 (10g): Your Key to a Flawless Matte Finish</h2>\r\n\r\n<p>Achieving a smooth, long-lasting matte look is essential for perfect makeup, and <strong>Cosmetics Matte to Last Pore Blurring Loose Powder Banana 03 (10g)</strong> is designed to do exactly that. This finely milled loose powder sets your makeup effortlessly while giving your skin a soft, natural, and pore-free appearance.</p>\r\n\r\n<h3>What Makes Banana 03 Loose Powder Special?</h3>\r\n\r\n<p>Banana loose powders are known for their subtle yellow undertone that helps brighten the complexion and balance uneven skin tones. The <strong>Banana 03 shade</strong> is especially suitable for Indian and medium skin tones, delivering a radiant yet natural finish without looking cakey.</p>\r\n\r\n<h3>Key Features &amp; Benefits</h3>\r\n\r\n<p><strong>✔ Long-Lasting Matte Finish</strong><br />\r\nKeeps your makeup fresh, matte, and shine-free throughout the day.</p>\r\n\r\n<p><strong>✔ Pore Blurring Effect</strong><br />\r\nVisibly minimizes pores and fine lines for a smooth, airbrushed look.</p>\r\n\r\n<p><strong>✔ Lightweight &amp; Comfortable</strong><br />\r\nUltra-light formula feels breathable on the skin and never heavy.</p>\r\n\r\n<p><strong>✔ Oil Control Formula</strong><br />\r\nAbsorbs excess oil, making it ideal for oily and combination skin types.</p>\r\n\r\n<p><strong>✔ Smooth Makeup Setting</strong><br />\r\nPerfectly sets foundation and concealer for an even, flawless finish.</p>\r\n\r\n<h3>How to Use</h3>\r\n\r\n<ol>\r\n	<li>\r\n	<p>After completing your base makeup, take a powder puff or fluffy brush</p>\r\n	</li>\r\n	<li>\r\n	<p>Pick a small amount of loose powder</p>\r\n	</li>\r\n	<li>\r\n	<p>Apply gently to under-eyes, T-zone, and oily areas</p>\r\n	</li>\r\n	<li>\r\n	<p>Dust off excess powder for a natural look</p>\r\n	</li>\r\n</ol>\r\n\r\n<h3>Who Is It For?</h3>\r\n\r\n<ul>\r\n	<li>\r\n	<p>Oily and combination skin types</p>\r\n	</li>\r\n	<li>\r\n	<p>Those looking for long-lasting, matte makeup</p>\r\n	</li>\r\n	<li>\r\n	<p>Anyone wanting to blur pores and control shine</p>\r\n	</li>\r\n	<li>\r\n	<p>Suitable for daily wear and professional makeup use</p>\r\n	</li>\r\n</ul>\r\n\r\n<h3>Why Choose Cosmetics Matte to Last Banana 03?</h3>\r\n\r\n<p>This loose powder not only sets your makeup but also enhances your skin&rsquo;s natural beauty. Its pore-blurring technology and oil-control formula ensure a polished look that lasts all day, making it a reliable addition to any makeup routine.</p>\r\n\r\n<h3>Final Verdict</h3>\r\n\r\n<p><strong>Cosmetics Matte to Last Pore Blurring Loose Powder Banana 03 (10g)</strong> is a must-have for anyone seeking a flawless matte finish with a natural glow. Affordable, lightweight, and highly effective, it deserves a place in every makeup kit.</p>', 'blog/4_uq7R5cA.jpg', '2026-01-17 18:29:18.768387', '2026-01-18 09:35:08.552462', 34, 0, 'active', 1, NULL, '', 1, 1, 2, 'Cosmetics, Makeup, Skincare, Herbal, Natural, Beauty, Matte, Powder Glow, Skin, Oil, Control, Pore, Blurring, Beauty, Care, Daily, Makeup,');

-- --------------------------------------------------------

--
-- Table structure for table `cms_blogcategory`
--

CREATE TABLE `cms_blogcategory` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `slug` varchar(100) NOT NULL,
  `description` longtext DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `order` int(11) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `parent_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cms_blogcategory`
--

INSERT INTO `cms_blogcategory` (`id`, `name`, `slug`, `description`, `image`, `is_active`, `order`, `created`, `updated`, `parent_id`) VALUES
(1, 'Bowls & Bonboniers', 'bowls-bonboniers', 'sdf', 'blog/categories/b7642f13605532612690a_a1.avif', 1, 1, '2025-12-10 20:02:35.594176', '2025-12-10 20:02:35.594176', NULL),
(2, 'Vases & Pots', 'vases-pots', 'sdff', 'blog/categories/db992ab8411061819838.avif', 1, 1, '2025-12-10 20:02:58.872868', '2025-12-10 20:02:58.873879', 1);

-- --------------------------------------------------------

--
-- Table structure for table `cms_cms`
--

CREATE TABLE `cms_cms` (
  `id` bigint(20) NOT NULL,
  `pagename` varchar(150) DEFAULT NULL,
  `Content` longtext DEFAULT NULL,
  `pageimage` varchar(100) DEFAULT NULL,
  `slug` varchar(200) DEFAULT NULL,
  `post_date` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `viewcounter` int(11) DEFAULT NULL,
  `post_status` int(11) DEFAULT NULL,
  `order` int(11) DEFAULT NULL,
  `status` varchar(8) NOT NULL,
  `author_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cms_cms`
--

INSERT INTO `cms_cms` (`id`, `pagename`, `Content`, `pageimage`, `slug`, `post_date`, `updated_at`, `viewcounter`, `post_status`, `order`, `status`, `author_id`) VALUES
(1, 'FAQ', '<p>No Newsasdsad</p>', 'cms/Screenshot_2026-01-06_134852_jaZPBd2.png', 'faq', '2026-01-09 20:04:42.575562', '2026-01-09 20:04:42.575562', 0, 100, 5, 'active', 1),
(2, 'Privacy Policy', '<p>At <strong>Mriigg</strong>, your privacy is important to us. This Privacy Policy explains how we collect, use, protect, and share your information when you visit or make a purchase from <a href=\"https://mriigg.com\"><strong>https://mriigg.com</strong></a> (the &ldquo;Website&rdquo;).</p>\r\n\r\n<p>By accessing or using our Website, you agree to the practices described in this policy.</p>\r\n\r\n<p><strong>1. Information We Collect</strong></p>\r\n\r\n<p><strong>Personal Information</strong></p>\r\n\r\n<p>When you interact with our Website, we may collect the following personal information:</p>\r\n\r\n<ul>\r\n	<li>Full name</li>\r\n	<li>Email address</li>\r\n	<li>Phone number</li>\r\n	<li>Billing and shipping address</li>\r\n	<li>Payment information (processed securely via third-party payment gateways)</li>\r\n	<li>Order and transaction history</li>\r\n</ul>\r\n\r\n<p><strong>2. How We Use Your Information</strong></p>\r\n\r\n<p>We use the information we collect to:</p>\r\n\r\n<ul>\r\n	<li>Process, fulfill, and deliver your orders</li>\r\n	<li>Communicate with you regarding orders, support, and inquiries</li>\r\n	<li>Improve our products, services, and website experience</li>\r\n	<li>Send promotional emails, offers, or updates (you may opt out at any time)</li>\r\n	<li>Prevent fraud and ensure website security</li>\r\n	<li>Comply with legal and regulatory requirements</li>\r\n</ul>\r\n\r\n<p><strong>3. Cookies &amp; Tracking Technologies</strong></p>\r\n\r\n<p>We use cookies and similar technologies to:</p>\r\n\r\n<ul>\r\n	<li>Enhance website functionality and performance</li>\r\n	<li>Understand user behavior and website traffic</li>\r\n	<li>Personalize content and marketing communications</li>\r\n</ul>\r\n\r\n<p>You can manage or disable cookies through your browser settings. Please note that disabling cookies may affect certain features of the Website.</p>\r\n\r\n<p><strong>4. Sharing of Information</strong></p>\r\n\r\n<p>We do <strong>not sell or rent</strong> your personal information.</p>\r\n\r\n<p>We may share your information only with trusted third parties, including:</p>\r\n\r\n<ul>\r\n	<li>Payment processing partners</li>\r\n	<li>Shipping and logistics providers</li>\r\n	<li>Website analytics and marketing service providers</li>\r\n	<li>Legal or regulatory authorities when required by law</li>\r\n</ul>\r\n\r\n<p>All third parties are required to protect your data and use it only for authorized purposes.</p>\r\n\r\n<p><strong>5. Data Security</strong></p>\r\n\r\n<p>We implement appropriate technical and organizational security measures to protect your personal information against unauthorized access, loss, misuse, or disclosure. While no online platform is completely secure, we take reasonable steps to safeguard your data.</p>\r\n\r\n<p><strong>6. Your Rights</strong></p>\r\n\r\n<p>Depending on applicable laws, you may have the right to:</p>\r\n\r\n<ul>\r\n	<li>Access the personal information we hold about you</li>\r\n	<li>Request correction or deletion of your data</li>\r\n	<li>Withdraw consent for marketing communications</li>\r\n	<li>Request data portability where applicable</li>\r\n</ul>\r\n\r\n<p>To exercise these rights, please contact us using the details provided below.</p>\r\n\r\n<p><strong>7. Third-Party Links</strong></p>\r\n\r\n<p>Our Website may contain links to third-party websites. Mriigg is not responsible for the privacy practices or content of those websites. We encourage you to review their privacy policies before sharing any personal information.</p>\r\n\r\n<p><strong>8. Children&rsquo;s Privacy</strong></p>\r\n\r\n<p>Mriigg does not knowingly collect personal information from children under the age of 13. If we become aware that such data has been collected, we will take steps to delete it promptly.</p>\r\n\r\n<p><strong>9. Changes to This Privacy Policy</strong></p>\r\n\r\n<p>We may update this Privacy Policy from time to time to reflect changes in our practices or legal obligations. Updates will be posted on this page with a revised effective date.</p>\r\n\r\n<p><strong>10. Contact Us</strong></p>\r\n\r\n<p>If you have any questions or concerns about this Privacy Policy or our data practices, please contact us:</p>', 'cms/m2.jpg', 'privacy-policy', '2026-01-10 10:22:37.166909', '2026-01-10 12:13:23.265266', 0, 100, 5, 'active', 1),
(3, 'About Us', '<p><strong>Mriigg &mdash; Clean Beauty. Thoughtful Care. Everyday Luxury.</strong></p>\r\n\r\n<p>At Mriigg, we believe self-care should feel both effective and indulgent. Born from a desire to bring salon-quality performance into daily routines, Mriigg creates thoughtfully formulated skin, hair, and body care &mdash; plus a pared-back makeup essential &mdash; that make everyday rituals simpler, better, and more beautiful.</p>\r\n\r\n<p><strong>Our Purpose</strong></p>\r\n\r\n<p>We design products that solve real needs without fuss. Whether it&rsquo;s restoring softness to feet, repairing hair between salon visits, or building a gentle morning skincare ritual, every Mriigg product is made to deliver visible benefits while still feeling luxurious.</p>\r\n\r\n<p><strong>What We Offer</strong></p>\r\n\r\n<p>Mriigg&rsquo;s collections focus on five core areas, each developed to work together or stand alone depending on your routine.</p>\r\n\r\n<p><strong>Skin Care</strong></p>\r\n\r\n<p>Bath salts, body gels, body lotions, body washes, massage oils, and artisan soaps &mdash; curated to cleanse, hydrate, and restore skin from head to toe. Lightweight, absorbent, and sensory-forward, our body range turns simple care into a ritual.</p>\r\n\r\n<p><strong>Hair Care</strong></p>\r\n\r\n<p>Shampoos, conditioners, nourishing hair masks, targeted hair oils, and serums formulated to strengthen, smooth, and revive. We balance performance with gentle care so hair looks polished without feeling weighed down.</p>\r\n\r\n<p><strong>Heel Care</strong></p>\r\n\r\n<p>A concentrated heel-care cream created to hydrate, repair, and soften rough or cracked skin. Easy to apply and fast-absorbing, it&rsquo;s designed for regular use until heels feel renewed.</p>\r\n\r\n<p><strong>Face Care</strong></p>\r\n\r\n<p>A compact face collection &mdash; cleansers, a dry cream, nourishing face oil, and a purifying face pack &mdash; developed to support balanced, healthy-looking skin. Each product is designed to slot into simple morning and evening routines.</p>\r\n\r\n<p><strong>Makeup</strong></p>\r\n\r\n<p>A single, high-quality eyeliner &mdash; refined, reliable, and flattering. It&rsquo;s the little makeup piece that finishes a look without complicating it.</p>\r\n\r\n<p><strong>Our Approach to Formulation</strong></p>\r\n\r\n<p>We combine proven actives with gentle, thoughtfully chosen ingredients. Our formulas are:</p>\r\n\r\n<ul>\r\n	<li>Designed for efficacy and comfort</li>\r\n	<li>Free from unnecessary harsh additives wherever possible</li>\r\n	<li>Created to pair well together so layering is simple and predictable</li>\r\n</ul>\r\n\r\n<p>We take care to craft balanced formulas that respect skin and hair&rsquo;s natural needs, and we continually refine recipes based on customer feedback and quality testing.</p>\r\n\r\n<p><strong>Quality &amp; Safety</strong></p>\r\n\r\n<p>Quality matters. Mriigg sources ingredients from vetted suppliers and manufactures to high standards. While we produce with care and follow good manufacturing practices, we always recommend patch testing a new product if you have sensitive skin or specific allergies.</p>\r\n\r\n<p><strong>Sustainability &amp; Packaging</strong></p>\r\n\r\n<p>We&rsquo;re mindful about packaging and waste. Wherever possible, we use recyclable materials and make choices that reduce unnecessary packaging. We&rsquo;re constantly exploring ways to improve &mdash; from refill options to cleaner supply chains &mdash; while keeping product performance front and center.</p>\r\n\r\n<p><strong>Who We Serve</strong></p>\r\n\r\n<p>Mriigg is for people who want better results with less complication &mdash; busy professionals, beauty minimalists, ritual lovers, and anyone who values products that feel premium without being precious. Our ranges are designed to address common everyday concerns across a variety of skin and hair types.</p>\r\n\r\n<p><strong>Our Values</strong></p>\r\n\r\n<ul>\r\n	<li><strong>Simplicity:</strong> Products that do the job without complexity.</li>\r\n	<li><strong>Integrity:</strong> Honest ingredients, clear labeling, and responsible sourcing.</li>\r\n	<li><strong>Pleasure:</strong> Textures and scents that make routines enjoyable.</li>\r\n	<li><strong>Care:</strong> Customer-first service and a commitment to continuous improvement.</li>\r\n</ul>', '', 'about-us', '2026-01-10 12:13:00.873647', '2026-01-10 12:13:00.873670', 4, 100, 5, 'active', 1),
(4, 'Shipping Policy', '<p>At <strong>Mriigg</strong>, we are committed to delivering your beauty and personal care products safely and on time. Please review our Shipping Policy to understand how orders are processed and shipped.</p>\r\n\r\n<p><strong>1. Order Processing Time</strong></p>\r\n\r\n<ul>\r\n	<li>All orders are processed within <strong>1&ndash;3 business days</strong>, excluding Sundays and public holidays.</li>\r\n	<li>Orders placed after business hours or during holidays will be processed on the next business day.</li>\r\n	<li>During promotional periods or high-volume sales, processing times may be slightly extended.</li>\r\n</ul>\r\n\r\n<p>Once your order is processed, you will receive an order confirmation and shipping details.</p>\r\n\r\n<p><strong>2. Shipping Locations</strong></p>\r\n\r\n<p>Currently, Mriigg ships to:</p>\r\n\r\n<ul>\r\n	<li><strong>All major locations within India</strong></li>\r\n</ul>\r\n\r\n<p>International shipping may be introduced in the future.</p>\r\n\r\n<p><strong>3. Shipping Charges</strong></p>\r\n\r\n<ul>\r\n	<li>Shipping charges, if applicable, are calculated and displayed at checkout.</li>\r\n	<li>Any free shipping offers will be clearly mentioned on the Website during promotional periods.</li>\r\n</ul>\r\n\r\n<p><strong>4. Estimated Delivery Time</strong></p>\r\n\r\n<p>Delivery timelines begin once the order has been shipped.</p>\r\n\r\n<ul>\r\n	<li><strong>Standard Delivery:</strong> 3&ndash;7 business days, depending on your location</li>\r\n	<li>Delivery times may vary due to courier delays, weather conditions, or unforeseen circumstances.</li>\r\n</ul>\r\n\r\n<p><strong>5. Order Tracking</strong></p>\r\n\r\n<p>Once your order has been shipped, a tracking number will be shared via email or SMS, allowing you to monitor your shipment&rsquo;s status.</p>\r\n\r\n<p><strong>6. Incorrect Address &amp; Failed Delivery</strong></p>\r\n\r\n<ul>\r\n	<li>Please ensure all shipping details are accurate at the time of checkout.</li>\r\n	<li>Mriigg is not responsible for delays or non-delivery due to incorrect or incomplete addresses.</li>\r\n	<li>Orders returned to us due to address errors may incur additional reshipping charges.</li>\r\n</ul>\r\n\r\n<p><strong>7. Damaged, Missing, or Lost Shipments</strong></p>\r\n\r\n<ul>\r\n	<li>If your order arrives damaged or with missing items, please contact us within <strong>48 hours of delivery</strong> with photos of the package and products.</li>\r\n	<li>In the case of lost shipments, our team will coordinate with the courier partner to resolve the issue.</li>\r\n</ul>\r\n\r\n<p><strong>8. Delivery Delays</strong></p>\r\n\r\n<p>While we work with reliable courier partners, delivery delays may occasionally occur due to factors beyond our control. Mriigg is not liable for delays caused by courier companies or natural events.</p>', '', 'shipping-policy', '2026-01-10 12:14:03.413515', '2026-01-10 12:14:03.413547', 2, 100, 5, 'active', 1),
(5, 'Terms & Conditions', '<p>Welcome to <strong>Mriigg</strong>. These Terms &amp; Conditions govern your access to and use of&nbsp; and any products or services offered by Mriigg.</p>\r\n\r\n<p>By accessing or using this Website, you agree to be bound by these Terms. If you do not agree, please do not use our Website.</p>\r\n\r\n<p><strong>1. Use of the Website</strong></p>\r\n\r\n<ul>\r\n	<li>You must be at least <strong>18 years old</strong> or have parental/guardian consent to use this Website.</li>\r\n	<li>You agree to use the Website for lawful purposes only and not in violation of any applicable laws or regulations.</li>\r\n	<li>We reserve the right to refuse service to anyone for any reason at any time.</li>\r\n</ul>\r\n\r\n<p><strong>2. Products &amp; Services</strong></p>\r\n\r\n<ul>\r\n	<li>All product descriptions, prices, and availability are subject to change without notice.</li>\r\n	<li>We make every effort to display products accurately; however, we do not guarantee that colors, images, or descriptions will be error-free or fully accurate on all devices.</li>\r\n	<li>Mriigg reserves the right to limit quantities or discontinue products at any time.</li>\r\n</ul>\r\n\r\n<p><strong>3. Pricing &amp; Payments</strong></p>\r\n\r\n<ul>\r\n	<li>Prices are listed in <strong>[specify currency]</strong> unless stated otherwise.</li>\r\n	<li>Payment must be completed at checkout through our approved payment gateways.</li>\r\n	<li>We reserve the right to correct pricing errors and cancel orders affected by incorrect pricing.</li>\r\n</ul>\r\n\r\n<p><strong>4. Order Acceptance &amp; Cancellation</strong></p>\r\n\r\n<ul>\r\n	<li>An order is considered accepted only after payment confirmation and shipment.</li>\r\n	<li>We reserve the right to cancel or refuse any order due to stock unavailability, pricing errors, suspected fraud, or other issues.</li>\r\n	<li>If an order is canceled after payment, a refund will be processed according to our Refund Policy.</li>\r\n</ul>\r\n\r\n<p><strong>5. Shipping &amp; Delivery</strong></p>\r\n\r\n<ul>\r\n	<li>Shipping times and fees are outlined in our <strong>Shipping Policy</strong>.</li>\r\n	<li>Delivery timelines are estimates and may vary due to external factors beyond our control.</li>\r\n	<li>Mriigg is not responsible for delays caused by shipping carriers or customs clearance.</li>\r\n</ul>\r\n\r\n<p><strong>6. Returns &amp; Refunds</strong></p>\r\n\r\n<ul>\r\n	<li>Returns, exchanges, and refunds are governed by our <strong>Refund &amp; Return Policy</strong>.</li>\r\n	<li>Certain products may be non-returnable due to hygiene or safety reasons.</li>\r\n</ul>\r\n\r\n<p><strong>7. Intellectual Property</strong></p>\r\n\r\n<ul>\r\n	<li>All content on this Website, including logos, images, text, graphics, and designs, is the property of Mriigg and is protected by intellectual property laws.</li>\r\n	<li>You may not copy, reproduce, distribute, or use any content without prior written permission.</li>\r\n</ul>\r\n\r\n<p><strong>8. User Content &amp; Reviews</strong></p>\r\n\r\n<ul>\r\n	<li>By submitting reviews or content, you grant Mriigg a non-exclusive, royalty-free right to use, display, and publish such content.</li>\r\n	<li>We reserve the right to remove any content that is offensive, misleading, or violates these Terms.</li>\r\n</ul>\r\n\r\n<p><strong>9. Limitation of Liability</strong></p>\r\n\r\n<ul>\r\n	<li>Mriigg shall not be liable for any indirect, incidental, or consequential damages arising from the use of our Website or products.</li>\r\n	<li>Our total liability shall not exceed the amount paid for the product purchased.</li>\r\n</ul>\r\n\r\n<p><strong>10. Indemnification</strong></p>\r\n\r\n<p>You agree to indemnify and hold harmless Mriigg from any claims, damages, or expenses arising from your use of the Website or violation of these Terms.</p>\r\n\r\n<p><strong>11. Privacy</strong></p>\r\n\r\n<p>Your use of the Website is also governed by our <strong>Privacy Policy</strong>, which explains how we collect and use your information.</p>\r\n\r\n<p><strong>12. Governing Law</strong></p>\r\n\r\n<p>These Terms shall be governed and interpreted in accordance with the laws of, without regard to conflict of law principles.</p>\r\n\r\n<p><strong>13. Changes to Terms</strong></p>\r\n\r\n<p>We reserve the right to update or modify these Terms at any time. Changes will be effective upon posting on this page.</p>', '', 'terms-conditions', '2026-01-10 12:14:31.031766', '2026-01-10 12:14:31.031786', 1, 100, 5, 'active', 1),
(6, 'Returns & Refunds Policy', '<p>At <strong>Mriigg</strong>, we want you to be satisfied with your purchase. Due to the personal and hygiene-sensitive nature of our products, please review our Returns &amp; Refunds Policy carefully before placing an order.</p>\r\n\r\n<p><strong>1. Return Eligibility</strong></p>\r\n\r\n<p>Returns are accepted only under the following conditions:</p>\r\n\r\n<ul>\r\n	<li>The product is <strong>unused, unopened, and in its original packaging</strong></li>\r\n	<li>The return request is raised within <strong>7 days</strong> of delivery</li>\r\n	<li>Proof of purchase (order ID or invoice) is provided</li>\r\n</ul>\r\n\r\n<p><strong>Important:</strong> Opened, used, or tampered products cannot be returned due to hygiene and safety reasons.</p>\r\n\r\n<p><strong>2. Non-Returnable Products</strong></p>\r\n\r\n<p>The following items are <strong>non-returnable and non-refundable</strong>:</p>\r\n\r\n<ul>\r\n	<li>Opened or used skincare, haircare, heel care, or cosmetic products</li>\r\n	<li>Products damaged due to customer misuse or negligence</li>\r\n	<li>Items marked as <strong>Final Sale / Non-Returnable</strong></li>\r\n	<li>Gift cards or promotional/free items</li>\r\n</ul>\r\n\r\n<p><strong>3. Damaged, Defective, or Incorrect Products</strong></p>\r\n\r\n<p>If you receive a product that is damaged, leaking, defective, or incorrect:</p>\r\n\r\n<ul>\r\n	<li>Contact us within <strong>48 hours</strong> of delivery</li>\r\n	<li>Share clear photos or videos of the product, outer box, and invoice</li>\r\n</ul>\r\n\r\n<p>After verification, we will arrange a <strong>replacement or refund</strong>, depending on product availability.</p>\r\n\r\n<p><strong>4. How to Request a Return</strong></p>\r\n\r\n<p>To initiate a return request:</p>\r\n\r\n<ol>\r\n	<li>Email us at <strong>Info@mriigg.com</strong></li>\r\n	<li>Mention your <strong>order number</strong>, product name, and reason for return</li>\r\n	<li>Attach images or videos (if applicable)</li>\r\n</ol>\r\n\r\n<p>Our support team will review your request and provide further instructions.</p>\r\n\r\n<p>Returns sent without prior approval may not be accepted.</p>\r\n\r\n<p><strong>5. Return Shipping</strong></p>\r\n\r\n<ul>\r\n	<li>Customers are responsible for return shipping costs unless the product is damaged or incorrect</li>\r\n	<li>We recommend using a trackable courier service</li>\r\n	<li>Mriigg is not responsible for items lost or damaged during return transit</li>\r\n</ul>\r\n\r\n<p><strong>6. Refund Process</strong></p>\r\n\r\n<ul>\r\n	<li>Once the returned item is received and inspected, we will notify you of approval or rejection</li>\r\n	<li>Approved refunds will be processed within <strong>7&ndash;10 business days</strong></li>\r\n	<li>Refunds will be issued to the <strong>original payment method</strong></li>\r\n</ul>\r\n\r\n<p>Shipping charges are <strong>non-refundable</strong>, except in cases of damaged or incorrect items.</p>\r\n\r\n<p><strong>7. Late or Missing Refunds</strong></p>\r\n\r\n<p>If you haven&rsquo;t received your refund after the stated processing time:</p>\r\n\r\n<ul>\r\n	<li>Check with your bank or payment provider</li>\r\n	<li>Contact us for assistance if the issue persists</li>\r\n</ul>\r\n\r\n<p><strong>8. Order Cancellations</strong></p>\r\n\r\n<ul>\r\n	<li>Orders can be canceled <strong>only before dispatch</strong></li>\r\n	<li>Once an order has been shipped, it cannot be canceled and will follow the return policy</li>\r\n</ul>\r\n\r\n<p><strong>9. Product Reactions Disclaimer</strong></p>\r\n\r\n<ul>\r\n	<li>Individual skin or hair reactions may vary</li>\r\n	<li>We strongly recommend performing a <strong>patch test</strong> before using any product</li>\r\n	<li>Mriigg is not responsible for reactions due to allergies, sensitivity, or improper use</li>\r\n</ul>\r\n\r\n<p><strong>10. Contact Us</strong></p>\r\n\r\n<p>For any questions related to returns or refunds, please contact us:</p>\r\n\r\n<p><strong>Email:</strong> Info@mriigg.com<br />\r\n<strong>Customer Care:</strong> +91 99961 58166</p>', '', 'returns-refunds-policy', '2026-01-10 12:15:15.876521', '2026-01-10 12:15:15.876547', 1, 100, 5, 'active', 1),
(7, 'Contact Us', '<p>We&rsquo;d love to hear from you! Whether you have a question about our products, need assistance with an order, or want to explore business opportunities, the Mriigg team is here to help.</p>\r\n\r\n<p>📞<strong> Contact Numbers</strong></p>\r\n\r\n<p><strong>Customer Care:</strong><br />\r\n📱<strong> +91 99961 58166</strong></p>\r\n\r\n<p><strong>Sales &amp; Marketing:</strong><br />\r\n📱<strong> +91 99961 58966</strong></p>\r\n\r\n<p><strong>Our team is available to assist you during business hours.</strong></p>\r\n\r\n<p>📧<strong> Email Us</strong></p>\r\n\r\n<p><strong>For general inquiries, support, or feedback, reach out to us at:</strong><br />\r\n✉️<strong> Info@mriigg.com</strong></p>\r\n\r\n<p><strong>We aim to respond to all emails as quickly as possible.</strong></p>\r\n\r\n<p>🕒<strong> Business Hours</strong></p>\r\n\r\n<p><strong>Monday &ndash; Saturday: 10:00 AM &ndash; 6:00 PM<br />\r\nSunday &amp; Public Holidays: Closed</strong></p>\r\n\r\n<p>🤝<strong> We&rsquo;re Here for You</strong></p>\r\n\r\n<p><strong>At Mriigg, customer satisfaction is our priority. Don&rsquo;t hesitate to get in touch &mdash; whether it&rsquo;s about fragrance recommendations, order support, or collaboration opportunities.</strong></p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p><strong>Social Media Link&nbsp;</strong></p>\r\n\r\n<p><strong>Facebook - </strong><a href=\"https://www.facebook.com/mriiggofficial\"><strong>https://www.facebook.com/mriiggofficial</strong></a></p>\r\n\r\n<p><strong>Instagram - </strong><a href=\"https://www.instagram.com/mriiggofficial/\"><strong>https://www.instagram.com/mriiggofficial/</strong></a><strong>&nbsp;</strong></p>\r\n\r\n<p><strong>X.Com - </strong><a href=\"https://x.com/Mriiggofficial\"><strong>https://x.com/Mriiggofficial</strong></a><strong>&nbsp;</strong></p>\r\n\r\n<p><strong>LinkedIn&nbsp; - </strong><a href=\"https://www.linkedin.com/company/mriigg\"><strong>https://www.linkedin.com/company/mriigg</strong></a><strong>&nbsp;</strong></p>', '', 'contact-us', '2026-01-10 12:16:01.700521', '2026-01-10 12:16:01.700542', 6, 100, 5, 'active', 1);

-- --------------------------------------------------------

--
-- Table structure for table `cms_profile_setting`
--

CREATE TABLE `cms_profile_setting` (
  `id` bigint(20) NOT NULL,
  `logo_light` varchar(100) DEFAULT NULL,
  `logo_dark` varchar(100) DEFAULT NULL,
  `footer_img` varchar(100) DEFAULT NULL,
  `body_img` varchar(100) DEFAULT NULL,
  `background_theme_light` varchar(7) DEFAULT NULL,
  `background_theme_dark` varchar(7) DEFAULT NULL,
  `container_background` varchar(7) DEFAULT NULL,
  `items_background` varchar(7) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `phone_number1` varchar(20) DEFAULT NULL,
  `phone_number2` varchar(20) DEFAULT NULL,
  `facbook` varchar(200) DEFAULT NULL,
  `instagram` varchar(200) DEFAULT NULL,
  `twitter` varchar(200) DEFAULT NULL,
  `linkedin` varchar(200) DEFAULT NULL,
  `youtube` varchar(200) DEFAULT NULL,
  `main_office_address` longtext DEFAULT NULL,
  `branch_office_address` longtext DEFAULT NULL,
  `google_map` longtext DEFAULT NULL,
  `copyright` varchar(255) DEFAULT NULL,
  `establish_at` date DEFAULT NULL,
  `create_date` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `status` varchar(8) NOT NULL,
  `author_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cms_profile_setting`
--

INSERT INTO `cms_profile_setting` (`id`, `logo_light`, `logo_dark`, `footer_img`, `body_img`, `background_theme_light`, `background_theme_dark`, `container_background`, `items_background`, `email`, `phone_number1`, `phone_number2`, `facbook`, `instagram`, `twitter`, `linkedin`, `youtube`, `main_office_address`, `branch_office_address`, `google_map`, `copyright`, `establish_at`, `create_date`, `updated_at`, `status`, `author_id`) VALUES
(1, 'logo/logo1.svg', 'logo/logo1_YrkJPYf.svg', '', '', '#FFFFFF', '#000000', '#fcf8e7', '#FFFFFF', 'info@mriigg.com', '99961 58166', '99961 58966', 'https://www.facebook.com/mriiggofficial', 'https://www.instagram.com/mriiggofficial', 'https://x.com/Mriiggofficial', 'https://www.linkedin.com/company/mriigg', NULL, 'Eldeco County SCO-9 Second floor , Hi Street, Main GT Road, Sector-19, Sonipat, 131001', '', '', '© Copyright 2026 | All Rights Reserved by Blumtexs Pvt Ltd', '2025-01-01', '2026-01-17 09:56:05.134043', '2026-01-17 09:57:43.896318', 'active', 1);

-- --------------------------------------------------------

--
-- Table structure for table `cms_slider`
--

CREATE TABLE `cms_slider` (
  `id` bigint(20) NOT NULL,
  `sliderimage` varchar(100) DEFAULT NULL,
  `slug` varchar(200) DEFAULT NULL,
  `post_date` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `order` int(11) DEFAULT NULL,
  `status` varchar(8) NOT NULL,
  `author_id` int(11) NOT NULL,
  `slidercat_id` bigint(20) DEFAULT NULL,
  `ad_title` varchar(200) DEFAULT NULL,
  `ad_description` longtext DEFAULT NULL,
  `deal_type` varchar(50) DEFAULT NULL,
  `product_id` bigint(20) DEFAULT NULL,
  `ad_start_date` date DEFAULT NULL,
  `ad_end_date` date DEFAULT NULL,
  `slidervideo` varchar(100) DEFAULT NULL,
  `video_url` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cms_slider`
--

INSERT INTO `cms_slider` (`id`, `sliderimage`, `slug`, `post_date`, `updated_at`, `order`, `status`, `author_id`, `slidercat_id`, `ad_title`, `ad_description`, `deal_type`, `product_id`, `ad_start_date`, `ad_end_date`, `slidervideo`, `video_url`) VALUES
(1, 'slider/m3.jpg', 'spring-summer-collection', '2025-12-14 10:32:26.731356', '2026-01-17 12:00:48.258496', 3, 'active', 1, 1, 'Spring Summer Collection', 'Description for the slider advertisement', 'hot_deals', 1, '2025-12-14', '2026-03-28', '', NULL),
(2, 'slider/m1.jpg', 'spring-summer-collection-1', '2025-12-15 10:10:33.727907', '2026-01-17 09:16:08.946228', 3, 'active', 1, 3, 'Spring Summer Collection', 'Description for the slider advertisement Description for the slider advertisement', 'hot_deals', 3, '2025-12-15', '2025-12-19', '', NULL),
(5, '', 'mriigg-collection', '2026-01-17 11:54:41.871592', '2026-01-17 11:55:08.644671', 1, 'active', 1, 1, 'Mriigg Collection', 'Mriigg Collection Mriigg Collection', 'hot_deals', 2, '2026-01-17', '2026-08-17', 'slider/videos/Untitled_design_2.mp4', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2025-12-05 12:18:26.345536', '1', 'Mriig', 1, '[{\"added\": {}}]', 16, 1),
(2, '2025-12-05 12:28:26.749777', '1', 'Makeup', 1, '[{\"added\": {}}]', 7, 1),
(3, '2025-12-05 13:17:58.969219', '3', 'Makeup / Face Primer', 1, '[{\"added\": {}}]', 7, 1),
(4, '2025-12-05 13:18:54.942878', '4', 'Makeup / Concealer', 1, '[{\"added\": {}}]', 7, 1),
(5, '2025-12-05 13:19:27.192994', '4', 'Makeup / Concealer', 2, '[]', 7, 1),
(6, '2025-12-05 13:19:47.424557', '4', 'Makeup / Concealer', 2, '[{\"changed\": {\"fields\": [\"Category Image\"]}}]', 7, 1),
(7, '2025-12-05 14:23:06.179962', '1', 'Bowls & Bonboniers', 1, '[{\"added\": {}}, {\"added\": {\"name\": \"product image\", \"object\": \"Image for Bowls & Bonboniers\"}}, {\"added\": {\"name\": \"product variation\", \"object\": \"Bowls & Bonboniers - Product variations blue: 100ml\"}}, {\"added\": {\"name\": \"product detail section\", \"object\": \"Bowls & Bonboniers - Product detail sections\"}}]', 9, 1),
(8, '2025-12-05 14:24:10.542468', '1', 'Bowls & Bonboniers', 2, '[{\"added\": {\"name\": \"product image\", \"object\": \"Image for Bowls & Bonboniers\"}}, {\"added\": {\"name\": \"product variation\", \"object\": \"Bowls & Bonboniers - Product variations pink: 50ml\"}}]', 9, 1),
(9, '2025-12-10 20:02:35.625273', '1', 'Bowls & Bonboniers', 1, '[{\"added\": {}}]', 21, 1),
(10, '2025-12-10 20:02:58.916304', '2', 'Bowls & Bonboniers / Vases & Pots', 1, '[{\"added\": {}}]', 21, 1),
(11, '2025-12-14 10:32:26.765661', '1', 'Spring Summer Collection', 1, '[{\"added\": {}}]', 20, 1),
(12, '2025-12-14 11:39:05.454662', '1', 'Spring Summer Collection', 2, '[{\"changed\": {\"fields\": [\"Ad Description\", \"Deal Type\"]}}]', 20, 1),
(13, '2025-12-14 11:41:04.079931', '1', 'Spring Summer Collection', 2, '[{\"changed\": {\"fields\": [\"Slider Image (1400X520px)\"]}}]', 20, 1),
(14, '2025-12-14 12:02:11.017758', '2', 'Skin', 2, '[{\"changed\": {\"fields\": [\"Category Image\"]}}]', 7, 1),
(15, '2025-12-15 10:10:33.752914', '2', 'Spring Summer Collection', 1, '[{\"added\": {}}]', 20, 1),
(16, '2025-12-16 19:28:36.962461', '1', 'Bowls & Bonboniers', 2, '[{\"changed\": {\"fields\": [\"description\"]}}, {\"added\": {\"name\": \"product variation\", \"object\": \"Product variations bladk: 100\"}}, {\"changed\": {\"name\": \"product variation\", \"object\": \"Product variations blue: 100\", \"fields\": [\"Qty\", \"Unit\", \"Is SKU Code\", \"Color Code\"]}}, {\"changed\": {\"name\": \"product variation\", \"object\": \"Product variations pink: 50\", \"fields\": [\"Qty\", \"Unit\", \"Is SKU Code\", \"Color Code\"]}}, {\"added\": {\"name\": \"product detail section\", \"object\": \"Bowls & Bonboniers - Product detail sections2\"}}, {\"changed\": {\"name\": \"product detail section\", \"object\": \"Bowls & Bonboniers - Product detail sections\", \"fields\": [\"content\"]}}]', 9, 1),
(17, '2025-12-16 20:08:51.042161', '2', 'index.html', 1, '[{\"added\": {}}, {\"added\": {\"name\": \"product image\", \"object\": \"Image for index.html\"}}, {\"added\": {\"name\": \"product image\", \"object\": \"Image for index.html\"}}, {\"added\": {\"name\": \"product image\", \"object\": \"Image for index.html\"}}, {\"added\": {\"name\": \"product image\", \"object\": \"Image for index.html\"}}, {\"added\": {\"name\": \"product variation\", \"object\": \"Variation\"}}, {\"added\": {\"name\": \"product detail section\", \"object\": \"index.html - Product detail sections\"}}]', 9, 1),
(18, '2025-12-17 11:42:12.376377', '3', 'MOD Ghrit Kumari Hair Oil- hair growth with 100% Aloe Vera juice', 1, '[{\"added\": {}}, {\"added\": {\"name\": \"product image\", \"object\": \"Image for MOD Ghrit Kumari Hair Oil- hair growth with 100% Aloe Vera juice\"}}, {\"added\": {\"name\": \"product image\", \"object\": \"Image for MOD Ghrit Kumari Hair Oil- hair growth with 100% Aloe Vera juice\"}}, {\"added\": {\"name\": \"product image\", \"object\": \"Image for MOD Ghrit Kumari Hair Oil- hair growth with 100% Aloe Vera juice\"}}, {\"added\": {\"name\": \"product image\", \"object\": \"Image for MOD Ghrit Kumari Hair Oil- hair growth with 100% Aloe Vera juice\"}}, {\"added\": {\"name\": \"product variation\", \"object\": \"Product variations blue: 150\"}}, {\"added\": {\"name\": \"product detail section\", \"object\": \"MOD Ghrit Kumari Hair Oil- hair growth with 100% Aloe Vera juice - Description\"}}, {\"added\": {\"name\": \"product detail section\", \"object\": \"MOD Ghrit Kumari Hair Oil- hair growth with 100% Aloe Vera juice - Additional information\"}}]', 9, 1),
(19, '2025-12-17 14:28:31.985460', '4', 'Bowls & Bonboniers', 1, '[{\"added\": {}}, {\"added\": {\"name\": \"product image\", \"object\": \"Image for Bowls & Bonboniers\"}}, {\"added\": {\"name\": \"product variation\", \"object\": \"This is a short description of the product.: 150\"}}, {\"added\": {\"name\": \"product detail section\", \"object\": \"Bowls & Bonboniers - Product detail sections\"}}]', 9, 1),
(20, '2025-12-17 15:11:28.162667', '1', 'jbadmin', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 4, 1),
(21, '2025-12-17 15:11:57.174403', '1', 'mriiggadmin', 2, '[{\"changed\": {\"fields\": [\"Username\", \"First name\", \"Last name\"]}}]', 4, 1),
(22, '2025-12-17 15:14:35.126023', '2', 'Spring Summer Collection', 2, '[{\"changed\": {\"fields\": [\"Slider Image (1400X520px)\"]}}]', 20, 1),
(23, '2025-12-18 20:44:00.824932', '1', 'Concealer / Bowls & Bonboniers', 1, '[{\"added\": {}}]', 22, 1),
(24, '2025-12-19 07:28:37.970390', '2', 'mod', 1, '[{\"added\": {}}]', 16, 1),
(25, '2025-12-19 07:29:02.622290', '5', 'Bowls & Bonboniers1', 1, '[{\"added\": {}}]', 7, 1),
(26, '2025-12-19 07:29:26.760527', '2', 'Bowls & Bonboniers1 / Vases & Pots1', 1, '[{\"added\": {}}]', 22, 1),
(27, '2025-12-19 11:58:29.881599', '1', 'Mriigg', 1, '[{\"added\": {}}]', 16, 1),
(28, '2025-12-19 12:01:10.380168', '2', 'Mod', 1, '[{\"added\": {}}]', 16, 1),
(29, '2025-12-19 12:04:40.074459', '1', 'Makeup', 1, '[{\"added\": {}}]', 7, 1),
(30, '2025-12-19 12:05:51.024380', '1', 'Makeup / Foundation', 1, '[{\"added\": {}}]', 22, 1),
(31, '2025-12-19 12:07:02.639376', '2', 'Makeup / Loose Powder', 1, '[{\"added\": {}}]', 22, 1),
(32, '2025-12-19 12:16:42.584660', '1', 'Cosmetics Matte to Last Pore Blurring Loose Powder Banana 03 (10g)', 1, '[{\"added\": {}}, {\"added\": {\"name\": \"product image\", \"object\": \"Image for Cosmetics Matte to Last Pore Blurring Loose Powder Banana 03 (10g)\"}}, {\"added\": {\"name\": \"product image\", \"object\": \"Image for Cosmetics Matte to Last Pore Blurring Loose Powder Banana 03 (10g)\"}}, {\"added\": {\"name\": \"product image\", \"object\": \"Image for Cosmetics Matte to Last Pore Blurring Loose Powder Banana 03 (10g)\"}}, {\"added\": {\"name\": \"product image\", \"object\": \"Image for Cosmetics Matte to Last Pore Blurring Loose Powder Banana 03 (10g)\"}}, {\"added\": {\"name\": \"product detail section\", \"object\": \"Cosmetics Matte to Last Pore Blurring Loose Powder Banana 03 (10g) - Product detail sections\"}}]', 9, 1),
(33, '2025-12-19 14:37:53.078625', '5', 'Image for Cosmetics Matte to Last Pore Blurring Loose Powder Banana 03 (10g)', 1, '[{\"added\": {}}]', 11, 1),
(34, '2025-12-19 15:06:20.286770', '4', 'Image for Cosmetics Matte to Last Pore Blurring Loose Powder Banana 03 (10g)', 3, '', 11, 1),
(35, '2025-12-19 15:06:20.286770', '3', 'Image for Cosmetics Matte to Last Pore Blurring Loose Powder Banana 03 (10g)', 3, '', 11, 1),
(36, '2025-12-19 15:06:20.286770', '2', 'Image for Cosmetics Matte to Last Pore Blurring Loose Powder Banana 03 (10g)', 3, '', 11, 1),
(37, '2025-12-19 15:06:20.286770', '1', 'Image for Cosmetics Matte to Last Pore Blurring Loose Powder Banana 03 (10g)', 3, '', 11, 1),
(38, '2025-12-19 18:59:26.551334', '1', 'mriigg', 1, '[{\"added\": {}}]', 16, 1),
(39, '2025-12-19 19:00:00.215450', '2', 'Mod', 1, '[{\"added\": {}}]', 16, 1),
(40, '2025-12-19 19:01:12.172950', '3', 'Nykaa', 1, '[{\"added\": {}}]', 16, 1),
(41, '2025-12-19 19:02:19.745296', '4', 'Nivea', 1, '[{\"added\": {}}]', 16, 1),
(42, '2025-12-20 16:51:06.277600', '2', 'Skin', 2, '[{\"changed\": {\"fields\": [\"Category Image\"]}}]', 7, 1),
(43, '2025-12-20 16:51:16.327153', '3', 'Hair', 2, '[{\"changed\": {\"fields\": [\"Category Image\"]}}]', 7, 1),
(44, '2025-12-20 16:51:47.314571', '2', 'Spring Summer Collection', 2, '[{\"changed\": {\"fields\": [\"Product\"]}}]', 20, 1),
(45, '2025-12-20 16:52:14.591193', '1', 'Spring Summer Collection', 2, '[{\"changed\": {\"fields\": [\"Select Category\"]}}]', 20, 1),
(46, '2025-12-22 16:16:24.559616', '3', 'Hair Care', 2, '[{\"changed\": {\"fields\": [\"Name\", \"Slug\"]}}]', 7, 1),
(47, '2025-12-22 16:16:37.487391', '2', 'Skin care', 2, '[{\"changed\": {\"fields\": [\"Name\", \"Slug\"]}}]', 7, 1),
(48, '2025-12-22 17:06:36.813769', '4', 'Heel Care', 1, '[{\"added\": {}}]', 7, 1),
(49, '2025-12-22 17:07:23.404791', '5', 'Face Care', 1, '[{\"added\": {}}]', 7, 1),
(50, '2025-12-22 17:12:45.281782', '8', 'Hair Care / Hair Mask', 1, '[{\"added\": {}}]', 22, 1),
(51, '2025-12-22 17:13:18.531259', '9', 'Hair Care / Hair Serum', 1, '[{\"added\": {}}]', 22, 1),
(52, '2025-12-22 17:13:41.449389', '10', 'Hair Care / Hair Conditioner', 1, '[{\"added\": {}}]', 22, 1),
(53, '2025-12-22 17:14:10.744906', '11', 'Face Care / Day Cream', 1, '[{\"added\": {}}]', 22, 1),
(54, '2025-12-22 17:15:15.790970', '12', 'Face Care / Night Cream', 1, '[{\"added\": {}}]', 22, 1),
(55, '2025-12-22 17:15:27.742535', '13', 'Face Care / Under Eye Cream', 1, '[{\"added\": {}}]', 22, 1),
(56, '2025-12-22 17:15:44.888795', '14', 'Face Care / Face Wash', 1, '[{\"added\": {}}]', 22, 1),
(57, '2025-12-22 17:16:16.811836', '15', 'Face Care / face Serum', 1, '[{\"added\": {}}]', 22, 1),
(58, '2025-12-22 17:16:31.173313', '16', 'Face Care / Cleansers', 1, '[{\"added\": {}}]', 22, 1),
(59, '2025-12-22 17:16:43.575477', '17', 'Face Care / Sunscreen Lotion', 1, '[{\"added\": {}}]', 22, 1),
(60, '2025-12-22 17:17:01.909902', '18', 'Face Care / Face Pack', 1, '[{\"added\": {}}]', 22, 1),
(61, '2025-12-22 17:17:25.500941', '19', 'Face Care / face Scrubs', 1, '[{\"added\": {}}]', 22, 1),
(62, '2025-12-22 17:17:37.421079', '20', 'Face Care / Face Oil', 1, '[{\"added\": {}}]', 22, 1),
(63, '2025-12-22 17:17:51.090504', '21', 'Face Care / Facial Kit', 1, '[{\"added\": {}}]', 22, 1),
(64, '2025-12-22 17:18:11.291623', '22', 'Face Care / Rose Water', 1, '[{\"added\": {}}]', 22, 1),
(65, '2025-12-22 17:20:01.174030', '23', 'Heel Care / Heel Care Cream', 1, '[{\"added\": {}}]', 22, 1),
(66, '2025-12-22 17:21:46.298288', '24', 'Makeup / Lipstick – Liquid', 1, '[{\"added\": {}}]', 22, 1),
(67, '2025-12-22 17:22:04.491369', '25', 'Makeup / Eye Liner', 1, '[{\"added\": {}}]', 22, 1),
(68, '2025-12-22 17:22:18.849591', '26', 'Makeup / Mascara', 1, '[{\"added\": {}}]', 22, 1),
(69, '2025-12-22 17:24:32.170801', '27', 'Makeup / Liquid Sindoor', 1, '[{\"added\": {}}]', 22, 1),
(70, '2025-12-22 17:24:51.616468', '28', 'Makeup / Lipstick – Stick', 1, '[{\"added\": {}}]', 22, 1),
(71, '2025-12-22 17:29:07.309146', '29', 'Skin care / Soap', 1, '[{\"added\": {}}]', 22, 1),
(72, '2025-12-22 17:29:20.620818', '30', 'Skin care / Body Wash', 1, '[{\"added\": {}}]', 22, 1),
(73, '2025-12-22 17:29:34.789064', '31', 'Skin care / Massage Oil', 1, '[{\"added\": {}}]', 22, 1),
(74, '2025-12-22 17:29:51.990762', '32', 'Skin care / Bath Salt', 1, '[{\"added\": {}}]', 22, 1),
(75, '2025-12-22 17:30:12.710614', '33', 'Skin care / Body Gel', 1, '[{\"added\": {}}]', 22, 1),
(76, '2025-12-22 17:41:09.061830', '11', 'Nykaa Naturals Tea Tree & Neem Purifying & Hydrating Gel - Controls Oils, Acne & Uneven tone Skin', 1, '[{\"added\": {}}]', 9, 1),
(77, '2025-12-22 17:51:50.639237', '12', 'Nykaa Naturals Tea Tree Essential Oil For Acne & Hair Fall Control Solution - 100% Natural', 1, '[{\"added\": {}}]', 9, 1),
(78, '2025-12-22 17:53:39.204630', '16', 'Nykaa Naturals Tea Tree Essential Oil For Acne & Hair Fall Control Solution - 100% Natural - How To Use', 1, '[{\"added\": {}}]', 13, 1),
(79, '2025-12-22 18:00:40.117593', '13', 'Nykaa Naturals Jojoba 100% Pure Cold Pressed Face Oil-Deep Hydration & Nourishment - All Skin Types', 1, '[{\"added\": {}}]', 9, 1),
(80, '2025-12-22 18:01:23.639097', '17', 'Nykaa Naturals Jojoba 100% Pure Cold Pressed Face Oil-Deep Hydration & Nourishment - All Skin Types - How To Use', 1, '[{\"added\": {}}]', 13, 1),
(81, '2025-12-22 18:13:17.775558', '14', 'Nyassa Under The Ocean Rejuvenating Bath Salts', 1, '[{\"added\": {}}]', 9, 1),
(82, '2025-12-22 18:21:38.559388', '15', 'Nyassa Under The Ocean Hand And Body Moisturizer', 1, '[{\"added\": {}}]', 9, 1),
(83, '2025-12-22 18:22:28.041515', '18', 'Nyassa Under The Ocean Hand And Body Moisturizer - Ingredients', 1, '[{\"added\": {}}]', 13, 1),
(84, '2025-12-22 18:22:48.504022', '19', 'Nyassa Under The Ocean Hand And Body Moisturizer - How To Use', 1, '[{\"added\": {}}]', 13, 1),
(85, '2025-12-22 18:32:18.660513', '16', 'Nykaa SkinRX Ceramide Barrier Repair Face Moisturizer with SPF 15- All Skin Types', 1, '[{\"added\": {}}]', 9, 1),
(86, '2025-12-22 18:34:37.126856', '20', 'Nykaa SkinRX Ceramide Barrier Repair Face Moisturizer with SPF 15- All Skin Types - Ingredients', 1, '[{\"added\": {}}]', 13, 1),
(87, '2025-12-23 19:03:22.186527', '1', 'skin Bowls & Bonboniers: 100', 1, '[{\"added\": {}}]', 12, 1),
(88, '2025-12-24 17:24:27.252962', '2', 'Nykaa SkinRX Ceramide Barrier Repair Face Moisturizer with SPF 14: 200', 1, '[{\"added\": {}}]', 12, 1),
(89, '2025-12-24 17:27:35.671826', '3', 'MOD Ghrit Kumari Hair Oil- hair growth with 100% Aloe Vera juice 200: 200', 1, '[{\"added\": {}}]', 12, 1),
(90, '2025-12-24 17:30:36.555271', '4', 'Nyassa Under The Ocean 150g Bath Salts: 120', 1, '[{\"added\": {}}]', 12, 1),
(91, '2025-12-24 17:32:26.566942', '5', 'Nykaa Naturals Tea Tree Essential Oil For Acne & Hair Fall Control Solution: 5', 1, '[{\"added\": {}}]', 12, 1),
(92, '2025-12-24 17:34:20.830479', '6', 'Nykaa Naturals Tea Tree & Neem Purifying & Hydrating Gel - Controls Oils, Acne & Uneven: 50', 1, '[{\"added\": {}}]', 12, 1),
(93, '2025-12-24 17:35:50.916543', '7', 'NYX Professional Makeup Buttermelt Glaze Soft Glow Skin Tint + SPF 20: 20', 1, '[{\"added\": {}}]', 12, 1),
(94, '2025-12-24 17:38:33.700886', '8', 'NYX Professional Makeup Bare With Me Serum And Calm Concealer: 8.5', 1, '[{\"added\": {}}]', 12, 1),
(95, '2025-12-24 17:40:08.682511', '9', 'NYX Professional Makeup Bare With Me Serum And Calm Concealer - Beige', 2, '[]', 9, 1),
(96, '2026-01-09 20:04:42.608076', '1', 'FAQ', 1, '[{\"added\": {}}]', 18, 1),
(97, '2026-01-10 10:22:37.183387', '2', 'Privacy Policy', 1, '[{\"added\": {}}]', 18, 1),
(98, '2026-01-10 10:24:10.211575', '6', 'testing', 1, '[{\"added\": {}}]', 7, 1),
(99, '2026-01-10 10:24:21.714087', '6', 'testing', 3, '', 7, 1),
(100, '2026-01-10 12:13:00.875054', '3', 'About Us', 1, '[{\"added\": {}}]', 18, 1),
(101, '2026-01-10 12:13:23.276348', '2', 'Privacy Policy', 2, '[{\"changed\": {\"fields\": [\"Long Discretion\"]}}]', 18, 1),
(102, '2026-01-10 12:14:03.414527', '4', 'Shipping Policy', 1, '[{\"added\": {}}]', 18, 1),
(103, '2026-01-10 12:14:31.033152', '5', 'Terms & Conditions', 1, '[{\"added\": {}}]', 18, 1),
(104, '2026-01-10 12:15:15.878773', '6', 'Returns & Refunds Policy', 1, '[{\"added\": {}}]', 18, 1),
(105, '2026-01-10 12:16:01.701275', '7', 'Contact Us', 1, '[{\"added\": {}}]', 18, 1),
(106, '2026-01-17 08:57:39.553403', '3', 'Mriigg Collection', 1, '[{\"added\": {}}]', 20, 1),
(107, '2026-01-17 09:13:15.682306', '4', 'Mriigg Collection', 1, '[{\"added\": {}}]', 20, 1),
(108, '2026-01-17 09:14:26.812059', '3', 'Mriigg Collection', 2, '[]', 20, 1),
(109, '2026-01-17 09:15:41.737910', '4', 'Mriigg Collection', 2, '[{\"changed\": {\"fields\": [\"Order\"]}}]', 20, 1),
(110, '2026-01-17 09:16:08.963777', '2', 'Spring Summer Collection', 2, '[{\"changed\": {\"fields\": [\"Order\"]}}]', 20, 1),
(111, '2026-01-17 09:16:42.698357', '1', 'Spring Summer Collection', 2, '[{\"changed\": {\"fields\": [\"Order\"]}}]', 20, 1),
(112, '2026-01-17 09:56:05.136011', '1', '1', 1, '[{\"added\": {}}]', 19, 1),
(113, '2026-01-17 09:57:43.903050', '1', '1', 2, '[{\"changed\": {\"fields\": [\"Copyright\"]}}]', 19, 1),
(114, '2026-01-17 11:50:22.321321', '3', 'Mriigg Collection', 3, '', 20, 1),
(115, '2026-01-17 11:53:33.196708', '4', 'Mriigg Collection', 3, '', 20, 1),
(116, '2026-01-17 11:54:41.872595', '5', 'Mriigg Collection', 1, '[{\"added\": {}}]', 20, 1),
(117, '2026-01-17 11:55:08.647673', '5', 'Mriigg Collection', 2, '[{\"changed\": {\"fields\": [\"Order\"]}}]', 20, 1),
(118, '2026-01-17 12:00:48.260495', '1', 'Spring Summer Collection', 2, '[{\"changed\": {\"fields\": [\"Order\"]}}]', 20, 1),
(119, '2026-01-17 16:33:56.231612', '1', 'My Sunday | Homepage Top Banner', 1, '[{\"added\": {}}]', 28, 1),
(120, '2026-01-17 16:47:59.632949', '2', 'Hot Product | Homepage Top Banner', 1, '[{\"added\": {}}]', 28, 1),
(121, '2026-01-17 16:50:14.854650', '3', 'New Launch | Homepage Top Banner', 1, '[{\"added\": {}}]', 28, 1),
(122, '2026-01-17 16:50:45.633339', '2', 'Hot Product | Homepage Top Banner', 2, '[{\"changed\": {\"fields\": [\"Offer Title\", \"Offer slug\"]}}]', 28, 1),
(123, '2026-01-17 17:55:33.419372', '4', 'My Sunday | Homepage Top Banner', 1, '[{\"added\": {}}]', 28, 1),
(124, '2026-01-17 17:56:16.668864', '1', 'My Sunday | Homepage Top Banner', 3, '', 28, 1),
(125, '2026-01-17 17:57:10.545677', '4', 'My Sunday | Homepage Top Banner', 2, '[{\"changed\": {\"fields\": [\"Display Order\"]}}]', 28, 1),
(126, '2026-01-17 17:57:10.548674', '3', 'New Launch | Homepage Top Banner', 2, '[{\"changed\": {\"fields\": [\"Display Order\"]}}]', 28, 1),
(127, '2026-01-17 17:57:10.563670', '2', 'Hot Product | Homepage Top Banner', 2, '[{\"changed\": {\"fields\": [\"Display Order\"]}}]', 28, 1),
(128, '2026-01-17 18:01:46.609513', '4', 'My Sunday | Homepage Top Banner', 2, '[{\"changed\": {\"fields\": [\"Offer slug\"]}}]', 28, 1),
(129, '2026-01-17 18:05:15.936960', '4', 'My Sunday | Homepage Top Banner', 2, '[{\"changed\": {\"fields\": [\"Offer image\"]}}]', 28, 1),
(130, '2026-01-17 18:16:35.297221', '2', 'Hot Product | Homepage Top Banner', 2, '[{\"changed\": {\"fields\": [\"Is active\"]}}]', 28, 1),
(131, '2026-01-17 18:16:46.998285', '2', 'Hot Product | Homepage Top Banner', 2, '[{\"changed\": {\"fields\": [\"Is active\"]}}]', 28, 1),
(132, '2026-01-17 18:29:18.827480', '1', 'Cosmetics Matte to Last Pore Blurring Loose Powder Banana', 1, '[{\"added\": {}}]', 17, 1),
(133, '2026-01-18 08:12:42.492288', '1', 'Cosmetics Matte to Last Pore Blurring Loose Powder Banana', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 17, 1),
(134, '2026-01-18 09:35:08.583630', '1', 'Cosmetics Matte to Last Pore Blurring Loose Powder Banana', 2, '[{\"changed\": {\"fields\": [\"Tags\"]}}]', 17, 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(7, 'ecommerce', 'category'),
(8, 'ecommerce', 'order'),
(9, 'ecommerce', 'product'),
(10, 'ecommerce', 'orderitem'),
(11, 'ecommerce', 'productimage'),
(12, 'ecommerce', 'productvariation'),
(13, 'ecommerce', 'productdetailsection'),
(14, 'ecommerce', 'customuser'),
(15, 'ecommerce', 'contactmessage'),
(16, 'ecommerce', 'brand'),
(17, 'cms', 'blog'),
(18, 'cms', 'cms'),
(19, 'cms', 'profile_setting'),
(20, 'cms', 'slider'),
(21, 'cms', 'blogcategory'),
(22, 'ecommerce', 'subcategory'),
(23, 'ecommerce', 'useraddress'),
(24, 'api', 'emailotp'),
(25, 'ecommerce', 'coupon'),
(26, 'ecommerce', 'couponusage'),
(27, 'ecommerce', 'payment'),
(28, 'ecommerce', 'offer'),
(29, 'ecommerce', 'offerproduct');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-10-15 19:32:24.464802'),
(2, 'auth', '0001_initial', '2025-10-15 19:32:24.888111'),
(3, 'admin', '0001_initial', '2025-10-15 19:32:24.984005'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-10-15 19:32:25.000104'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-10-15 19:32:25.007183'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-10-15 19:32:25.065308'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-10-15 19:32:25.112734'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-10-15 19:32:25.140362'),
(9, 'auth', '0004_alter_user_username_opts', '2025-10-15 19:32:25.147865'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-10-15 19:32:25.185382'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-10-15 19:32:25.188382'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-10-15 19:32:25.189281'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-10-15 19:32:25.223801'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-10-15 19:32:25.253425'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-10-15 19:32:25.286163'),
(16, 'auth', '0011_update_proxy_permissions', '2025-10-15 19:32:25.294186'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-10-15 19:32:25.321810'),
(18, 'ecommerce', '0001_initial', '2025-10-15 19:32:25.493098'),
(19, 'ecommerce', '0002_remove_product_image_productimage', '2025-10-15 19:32:25.564826'),
(20, 'ecommerce', '0003_product_short_description', '2025-10-15 19:32:25.628614'),
(21, 'ecommerce', '0004_productvariation', '2025-10-15 19:32:25.685706'),
(22, 'ecommerce', '0005_alter_productvariation_unique_together', '2025-10-15 19:32:25.713947'),
(23, 'ecommerce', '0006_category_parent', '2025-10-15 19:32:25.756308'),
(24, 'ecommerce', '0007_productdetailsection', '2025-10-15 19:32:25.806398'),
(25, 'ecommerce', '0008_category_is_active_category_order_product_is_active_and_more', '2025-10-15 19:32:25.949813'),
(26, 'ecommerce', '0009_product_featured_product_latest_product_offerprice_and_more', '2025-10-15 19:32:26.126367'),
(27, 'ecommerce', '0010_alter_product_category_alter_product_offerprice_and_more', '2025-10-15 19:32:27.499084'),
(28, 'ecommerce', '0011_customuser', '2025-10-15 19:32:27.735928'),
(29, 'ecommerce', '0012_order_user', '2025-10-15 19:32:27.791593'),
(30, 'ecommerce', '0013_alter_customuser_first_name_and_more', '2025-10-15 19:32:27.874591'),
(31, 'ecommerce', '0014_contactmessage', '2025-10-15 19:32:27.890591'),
(32, 'sessions', '0001_initial', '2025-10-15 19:32:27.930591'),
(33, 'ecommerce', '0015_brand_product_brand', '2025-12-05 12:04:03.688137'),
(34, 'ecommerce', '0016_brand_image_brand_remark', '2025-12-05 12:12:54.239045'),
(35, 'ecommerce', '0017_category_image_category_created_category_updated', '2025-12-05 12:25:57.610880'),
(36, 'ecommerce', '0018_alter_category_options_alter_category_order_and_more', '2025-12-05 13:40:10.278113'),
(38, 'ecommerce', '0019_alter_productvariation_unique_together_and_more', '2025-12-05 14:29:24.511909'),
(39, 'ecommerce', '0020_productvariation_quantity_productvariation_unit_and_more', '2025-12-10 19:56:07.463776'),
(41, 'cms', '0001_initial', '2025-12-10 19:57:57.839172'),
(43, 'ecommerce', '0021_update_app_label', '2025-12-11 02:09:41.000000'),
(47, 'ecommerce', '0024_create_subcategory_and_update_product', '2025-12-19 02:05:17.000000'),
(48, 'ecommerce', '0024_create_subcategory_and_update_product', '2025-12-19 02:12:39.000000'),
(49, 'api', '0001_initial', '2025-12-28 19:51:33.207853'),
(50, 'api', '0002_alter_emailotp_id', '2025-12-28 19:51:33.212020'),
(51, 'ecommerce', '0002_delete_useraddress', '2025-12-28 20:12:11.191796'),
(57, 'ecommerce', '0003_useraddress', '2025-12-29 11:53:07.738936'),
(58, 'ecommerce', '0004_order_status', '2025-12-29 11:53:23.160058'),
(59, 'ecommerce', '0005_alter_order_status', '2025-12-29 11:53:23.168683'),
(60, 'ecommerce', '0006_orderitem_variation', '2025-12-29 11:53:40.635564'),
(61, 'ecommerce', '0007_order_discount_total_coupon_order_coupon_couponusage', '2025-12-29 11:54:00.120071'),
(68, 'ecommerce', '0007_payment', '2026-01-10 00:50:35.039299'),
(69, 'ecommerce', '0008_merge_20260103_1559', '2026-01-10 00:50:35.041170'),
(72, 'test_app', 'test_migration', '2026-01-10 00:51:30.904206'),
(73, 'cms', '0002_initial', '2026-01-09 19:22:55.322766'),
(74, 'cms', '0003_alter_profile_setting_logo_dark_and_more', '2026-01-09 19:22:55.326313'),
(75, 'cms', '0002_blogcategory_blog_category_blog_subcategory', '2026-01-10 00:54:26.702276'),
(76, 'cms', '0003_slider_ad_description_slider_ad_title_and_more', '2026-01-10 00:54:26.704274'),
(77, 'cms', '0004_slider_ad_start_date_slider_ad_end_date', '2026-01-10 00:54:26.706590'),
(78, 'cms', '0005_remove_slider_title_remove_slider_des', '2026-01-10 00:54:26.708310'),
(79, 'ecommerce', '0009_coupon_valid_products', '2026-01-09 19:37:42.601348'),
(81, 'ecommerce', '0010_order_coupons', '2026-01-09 19:39:22.335787'),
(82, 'cms', '0004_slider_slidervideo_slider_video_url_and_more', '2026-01-15 16:32:13.629468'),
(83, 'cms', '0005_alter_slider_options_alter_slider_deal_type', '2026-01-17 14:48:50.676720'),
(84, 'ecommerce', '0011_offer', '2026-01-17 14:48:50.711719'),
(85, 'ecommerce', '0012_offerproduct', '2026-01-17 15:15:53.819768'),
(86, 'ecommerce', '0013_populate_offer_meta_fields', '2026-01-17 17:48:16.985180'),
(87, 'ecommerce', '0014_alter_offer_meta_fields_required', '2026-01-17 17:49:09.537419'),
(88, 'ecommerce', '0015_alter_offer_options_offer_order', '2026-01-17 17:52:49.081511'),
(89, 'ecommerce', '0016_make_offer_image_required', '2026-01-17 18:15:15.920070'),
(90, 'cms', '0006_blog_tags', '2026-01-18 09:20:31.748600');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('ard9q1n9po5dq40n7h4hsrynh3i97etj', '.eJxVjMsOwiAQRf-FtSFAebp07zeQGRikaiAp7cr479qkC93ec859sQjbWuM2aIlzZmcm2el3Q0gPajvId2i3zlNv6zIj3xV-0MGvPdPzcrh_BxVG_dYle4_KOzKhWNJO24mKxxScNqKoCY3Xwk8QijTapEAkQaESDtFKoQx7fwDcVzdW:1vVtBY:2NscmnlTtSqAl9KuVnIqWU_cagocC8Jmvsc1Fs9Hv5c', '2025-12-31 15:11:28.173668'),
('rtp3fw7lo91g14c98tpo9g6iiiwt2njg', '.eJxVjMEOwiAQRP-FsyGl0MJ69N5vIAu7SNVAUtqT8d9tkx70OPPezFt43Nbst8aLn0lchRKX3y5gfHI5AD2w3KuMtazLHOShyJM2OVXi1-10_w4ytryvgY0ZERgG6ywyatTE7JKyDlwkA5SCpT13llSyAfqEThnNpodRD534fAH3NjgA:1vRULw:PtKoxTGvISGUNWa3eYLOEMYlGUn84lUHH6H2JXGqIu4', '2025-12-19 11:52:00.762606'),
('vqhxtudy4p5wwlhr4w8np0bo1hum8f3f', '.eJxVjMEOwiAQRP-FsyGl0MJ69N5vIAu7SNVAUtqT8d9tkx70OPPezFt43Nbst8aLn0lchRKX3y5gfHI5AD2w3KuMtazLHOShyJM2OVXi1-10_w4ytryvgY0ZERgG6ywyatTE7JKyDlwkA5SCpT13llSyAfqEThnNpodRD534fAH3NjgA:1vPaSq:sfp7pWx2Q5NsU8fI9cCcuNIPGOaUSYFIC_ygVxATh_g', '2025-12-14 05:59:16.376127'),
('xt3soc0wszth56c39mdgu6j3e2vtze3b', '.eJxVjMEOwiAQRP-FsyGl0MJ69N5vIAu7SNVAUtqT8d9tkx70OPPezFt43Nbst8aLn0lchRKX3y5gfHI5AD2w3KuMtazLHOShyJM2OVXi1-10_w4ytryvgY0ZERgG6ywyatTE7JKyDlwkA5SCpT13llSyAfqEThnNpodRD534fAH3NjgA:1vTPaN:5wqIRwjHKnvhKdyRNzZ3UAt5SZygNPv0DY4bk5wyJ4k', '2025-12-24 19:10:51.755177'),
('hgjioehvy48m3i5v5a9ewsyhp7esltvm', '.eJxVjMsOwiAQRf-FtSFAebp07zeQGRikaiAp7cr479qkC93ec859sQjbWuM2aIlzZmcm2el3Q0gPajvId2i3zlNv6zIj3xV-0MGvPdPzcrh_BxVG_dYle4_KOzKhWNJO24mKxxScNqKoCY3Xwk8QijTapEAkQaESDtFKoQx7fwDcVzdW:1vWfHz:WEeItmvmlIPMx3m0wcQOtS2FRjBG-_8T6xNgIoYYLE8', '2026-01-02 18:33:19.899891'),
('zihpslvtj6d0nzu5qousw3247ora80ne', '.eJxVjMsOwiAQRf-FtSFAebp07zeQGRikaiAp7cr479qkC93ec859sQjbWuM2aIlzZmcm2el3Q0gPajvId2i3zlNv6zIj3xV-0MGvPdPzcrh_BxVG_dYle4_KOzKhWNJO24mKxxScNqKoCY3Xwk8QijTapEAkQaESDtFKoQx7fwDcVzdW:1vX0A1:P_DA2r-wJ_oIwMC1cCnlQpTGt-5-oqrq_Djy_Uzo7fM', '2026-01-03 16:50:29.963177'),
('mxjvk0gcoahvylrwjvx757vwnk97ca67', 'eyJ3aXNobGlzdCI6WyIxIl19:1vYAXb:jKWwjFq40yxWRVfyyQ__dQ-FXDAwLNBZf3qDTaV_nao', '2026-01-06 22:07:39.163619'),
('1gaahnkyg295vse0bwjjo2u0ik3emulv', 'eyJjYXJ0Ijp7IjE1IjoxfX0:1vYB1T:J20S78nkW-HmNpvO-ai0kYOscKwe1DaL1mNArHvPq5A', '2026-01-06 22:38:31.216807'),
('rkk8w9b2xitqc0qqlo3zje5mp6fx94hf', 'eyJjYXJ0Ijp7IjE0IjoxfX0:1vYBV3:nZkPSdKtwX0jrEpMfN_C3hvx1-dIofzl_5PHCIlmP7g', '2026-01-06 23:09:05.002799'),
('wu035uiczi6mp6st8d7vado6xq4u2nnm', 'eyJjYXJ0Ijp7IjE2IjoxfX0:1vYBo9:ZmEEm0wF1Bak54Hip4p2oT-mBPOYqKW9KCuKDs4dVVs', '2026-01-06 23:28:49.069172'),
('cpdfpiv65a2pgf0qmhpeqw5ohxbryw23', 'eyJ3aXNobGlzdCI6WyI0Il19:1vYEGv:6CmBMBH8VClLjViu9y_hoGzG2kqUJD4cyEZv-qJUjek', '2026-01-07 02:06:41.793586'),
('qwlhc8qfumnbvg2sbgz8wm24tf7voaje', 'eyJ3aXNobGlzdCI6WyIxIl19:1vYF1G:KeCl008dk8DNtfJdCLqrKbSN6Qv8TXJrBVBqd6cF4kU', '2026-01-07 02:54:34.634537'),
('sh6unk5zymzh42gzbqedujxbhnltzm26', 'eyJ3aXNobGlzdCI6WyIxNiJdfQ:1vYFAx:2i85hzo6wV4EVSVTX5xkDa4otmZ_u8tz0gPkR_dwBhw', '2026-01-07 03:04:35.538434'),
('uac7a0qaoes16mhb466vneashsz3ya4j', 'eyJjYXJ0Ijp7IjExIjoxfX0:1vYFV1:vyYhFnbGQtddyBJdaHbc0zomwcgKdj8fPqur-VH6TYU', '2026-01-07 03:25:19.562144'),
('3l6dsir9iri6ybd5pgendbvmwe3skjj0', 'eyJjYXJ0Ijp7IjE1IjoxfX0:1vYFnb:uRhPvaHJKY-s7HKEHSusqT5Y8ktccR_4C07KUhZ-42c', '2026-01-07 03:44:31.328030'),
('a31uw7woho6x622z3dznyc9jk7e8e6o2', 'eyJ3aXNobGlzdCI6WyI3Il19:1vYqaO:Hvfq85aT9GEO4XqZj2O9ZyT55s60T7nM31bVlkisPhw', '2026-01-08 19:01:20.566098'),
('rbcvfzgh4xqnzu2782t27o2ymbral1j3', 'eyJ3aXNobGlzdCI6WyI2Il19:1vYqk0:x_A8SvYjXBjzXmVMrlvMOky3wiogm4jYv30Nc7Ri24I', '2026-01-08 19:11:16.164976'),
('ovs4rbiaa4h6dwwiwkirhjb6mytt9ajt', 'eyJ3aXNobGlzdCI6WyI5Il19:1vYr4T:sLIPpUbly6n4p0QtW48jsXV9LDC3dQSTKjdS1U1BWFo', '2026-01-08 19:32:25.723621'),
('i7x46uhd0k00jvygufzf8aatrbcs22kk', 'eyJjYXJ0Ijp7IjEwIjoxfX0:1vYrpq:viR6MdCwoR06pJH5oIYHLIm1DKEW9_OMnwe5NufG4YQ', '2026-01-08 20:21:22.407075'),
('ctvfbsuj8ccfuq8pkxsszpi3b4hk7136', 'eyJjYXJ0Ijp7IjEzIjoxfX0:1vYs0M:tDwgeO2E2s5b1tsHWMC6vG4Ve0Bwo5zdyPdzNRTO9ug', '2026-01-08 20:32:14.892507'),
('1szrf9zmxdb9tmmqxuv2lfx92ihmfay9', 'eyJjYXJ0Ijp7IjE0IjoxfX0:1vYs4W:l0vrUZujgbmlXvNwwVEWitg1Zj3z2YPNh08XVmbNUZo', '2026-01-08 20:36:32.569608'),
('6u4tdq0rd7cop15h9fqcsqnukx0fj475', 'eyJjYXJ0Ijp7IjEzIjoxfX0:1vYs4W:EpnzSuMO_mPhhDQmDY363Hc8_3fRq9wPmMiD9DqByQg', '2026-01-08 20:36:32.643712'),
('lo2sgsp8xngz3zf2q5sseruyoo4no7re', 'eyJjYXJ0Ijp7IjE1IjoxfX0:1vYs4W:WZPLPuFZpaSgUjf_0CIcvGUKylnHtkpxMAFBU0rywLs', '2026-01-08 20:36:32.655982'),
('yxzh0rss5xd42nst71lgv62u8kvi60pl', 'eyJjYXJ0Ijp7IjE2IjoxfX0:1vYs4X:UUfpt2ZERgA0Rl6V5JCREEvlX9kfaFe0niENsU9awTY', '2026-01-08 20:36:33.012974'),
('6nafk5dclfy0aa39cyhbph7e3jhhw7o5', 'eyJ3aXNobGlzdCI6WyI2Il19:1vYsww:fkqnClws0EY-Fu_GZSWHT3XfnM7SL8esd3bJdKuwnWA', '2026-01-08 21:32:46.196143'),
('2k5p5xdqacuq1wo4y3scwsheo7ssu3c1', 'eyJ3aXNobGlzdCI6WyI4Il19:1vYt4q:qqjc-93WXmQ51wL179A6OPvu6QazvLYNPfch6QM4VWE', '2026-01-08 21:40:56.878829'),
('5ew2lp7qmpo7d31sc7o3pljrs22rk6ne', 'eyJ3aXNobGlzdCI6WyI5Il19:1vYtPd:o6r5OeCmI_MUjWt2FGwYvZhS9PWQ7JyQH_0VyBxxUN8', '2026-01-08 22:02:25.717595'),
('xlizspfhqq1nh5y6kurhz4ubxh6wv7oc', 'eyJ3aXNobGlzdCI6WyI3Il19:1vYtYs:6Q9uGfvEnjfhH5P7pVdwuG5H2POpWuS90u24OzvUulg', '2026-01-08 22:11:58.026878'),
('5v1gvd1d1rtuy8wsevf3keqa3ltyu5gy', 'eyJ3aXNobGlzdCI6WyIxMCJdfQ:1vYtjy:_1_eqKJRYKSSIt7RezDOwBF5Gt0ihXILgOuuS61wzE4', '2026-01-08 22:23:26.054063'),
('fe8ht0vuxlr0510b2n36686bwex4t4bi', 'eyJ3aXNobGlzdCI6WyIxMSJdfQ:1vYtrr:hvSLlQheabeXrzrPD3zTqy4Rm3gkPEiDqjfWyXIwTmo', '2026-01-08 22:31:35.027879'),
('dv0vdforpgh40tx9dpkrx4q79fy2xyd8', 'eyJjYXJ0Ijp7IjExIjoxfX0:1vYu25:mtiOOcVNFySvUhZfxP8r-bOTGyIzRpi2K4DUirjyjyU', '2026-01-08 22:42:09.387977'),
('a3ngftjinupqe5u27vrvksd57cy9286l', 'eyJ3aXNobGlzdCI6WyIxMyJdfQ:1vYuLD:RSfugjcuHBxUJq-Rr_k1X1haf0OnYyoPOJ810IRF2Ec', '2026-01-08 23:01:55.958757'),
('1nyoiwhi900q9k8tcr9ak8pjem5uea1d', 'eyJ3aXNobGlzdCI6WyIxNSJdfQ:1vYuVb:Zpe9I06Ax8gv8W_ySMwGm1fSjpff6p0R4WtVIAlQ8a0', '2026-01-08 23:12:39.416718'),
('yypittp0426mzhw44rd16jl1xj390ywo', 'eyJjYXJ0Ijp7IjEzIjoxfX0:1vYugX:nsPh9NpSEwK3ZswF35kIzU5wDEJUFHccF5NlOTLJv8E', '2026-01-08 23:23:57.433212'),
('l3mceclg2yqzkx0xeaxlnp5lzltd4uen', 'eyJjYXJ0Ijp7IjEiOjF9fQ:1vZubw:zzjztsUvztNrT7OsldYf1JAeY1gh8eta9pYKXqnsdXk', '2026-01-11 17:31:20.528147'),
('ciy5ua37h0qm5n1rio16qftrg1uenw2f', '.eJxVjEEOwiAQRe_C2hAoQsGl-56BzDCMVA0kpV0Z765NutDtf-_9l4iwrSVuPS9xJnERWpx-N4T0yHUHdId6azK1ui4zyl2RB-1yapSf18P9OyjQy7f2Hh1ZTSaDReMtOD4DQ9bK2TAYpTiPbuCRtdUuUdDM3lhDAT2hYhTvD-h2ODo:1vaC2k:hExtAeB393o8a-ZIXceK5SF3hVlkCQCSOgJzYKJby8E', '2026-01-12 12:08:10.495096'),
('dtzl1b7jrlxsi9ve775ogz1eoek6aahy', 'eyJjYXJ0Ijp7IjE0IjoxfX0:1vaOGg:HgKgDJdNBredZKWyaucBdj59ycS7liLLYmOxbqOZeh0', '2026-01-13 01:11:22.094058'),
('aovb06pd1c0tyec2v5ycdg132m9dig8g', 'eyJjYXJ0Ijp7IjIiOjF9fQ:1vaRGM:B-LEq0xviJYSyuwWG3Gxk6E5OyM1M3DdDTKt8frfq7w', '2026-01-13 04:23:14.014171'),
('pli1pnmtu9jt69qub8bdglcpn7qjxq5t', 'eyJ3aXNobGlzdCI6WyIxMyJdfQ:1vaTr0:OGvhrqV1J2SQaKvweQ1WGq1DCWR6qJRzOAEjICUPFIs', '2026-01-13 07:09:14.219322'),
('tyllkbj7xfvp7kqkkbxm9jqi44w6kpq2', 'eyJ3aXNobGlzdCI6WyI4Il19:1vaU4n:p3VXeSKKucmhVF4Ei9E01DxoEsOmOFKnmyfaZ2A9YLM', '2026-01-13 07:23:29.254626'),
('aeysjuoq6oi7iayiwt0e9qpvckzavn81', 'eyJjYXJ0Ijp7IjEyIjoxfX0:1vaUCB:gZX_V9T1STtZaAm968SHevy-x5xML8K8384gYGqP73I', '2026-01-13 07:31:07.577176'),
('lzopvq0uooin46kt30alqarntk1gb2zl', 'eyJ3aXNobGlzdCI6WyIxMSJdfQ:1vaUNg:T_eJKXKEV3NfrpCB87h6LhOglH7JdLnyi7F0HxJY6e8', '2026-01-13 07:43:00.643838'),
('2eper97o6nbvi7cplkcqilegxcn1yhcn', 'eyJjYXJ0Ijp7IjciOjF9fQ:1vaUXC:VtAtaakaMJu5SRPCfTqpPn8UqdpI2QibYeENQKiqv_0', '2026-01-13 07:52:50.323241'),
('rah06b2l5egake45dfr4b71unzk485rn', 'eyJjYXJ0Ijp7IjE2IjoxfX0:1vaUgJ:SUlKvaAzmKHhidpVbTh6hhxEaUb97Pvdie0X0OCCGWE', '2026-01-13 08:02:15.509690'),
('elzwo71qhsw4h6vitj0kjuauuti8l3no', 'eyJ3aXNobGlzdCI6WyIxNSJdfQ:1vaUr2:LO5u_qNn_Sgxy5LaLcQO43Ccl25j38knaRRvAWRUg_s', '2026-01-13 08:13:20.448308'),
('luoaflwdtbjdrwjcsuzw1xlx0crkh3iq', 'eyJ3aXNobGlzdCI6WyI1Il19:1vafp5:mfGB4VkDa-0lGSJUW7PdnSLQItLF_sUKjheZVLzlM4w', '2026-01-13 19:56:03.709136'),
('1desng2ozhfshqe24u1tb1lgt7xp5kva', 'eyJ3aXNobGlzdCI6WyIxIl19:1vagRh:AtcgBqVdUcpvabFaRgoskYBUHIS6AQxXOgH0mNiI0cU', '2026-01-13 20:35:57.709255'),
('e9nribfyx7rsgnn4tmgrhzz4uoixu506', 'eyJjYXJ0Ijp7IjgiOjF9fQ:1vaguG:ub16C6ghIk0E_g6Klb4oG8NjhRMmfNy6w7XNYCErRWM', '2026-01-13 21:05:28.653572'),
('htfeab1utykp7ycr49a1g0zau62c6zc2', 'eyJ3aXNobGlzdCI6WyIxNiJdfQ:1vah4C:EpaZlwQEm0iX4wI4W86yPlzR2rik3QNtpEBO5SvX0Uo', '2026-01-13 21:15:44.589085'),
('w3nf079a49mv6gkehb4bwfrg6x7rri7e', 'eyJjYXJ0Ijp7IjIiOjF9fQ:1vahEm:CU-n24CnO4aI8pS4zuvnoSx8sayYq69wD8-mDEGHJuE', '2026-01-13 21:26:40.630476'),
('xav1r5sppwp36b88p3418n8qlhuale2g', 'eyJjYXJ0Ijp7IjExIjoxfX0:1vahKu:-ZN-UzMHGP7nUsCibfYPnurw-ZIAPf0-ILsCYPkvh9Y', '2026-01-13 21:33:00.388008'),
('dgk1u5hd3qg1u1djw0kz6ecxulr0g4ke', 'eyJjYXJ0Ijp7IjUiOjF9fQ:1vaiU8:FCvqsu6jdxwrmixGU-NPjX8-sBp5-zLEEseNATvVI1Q', '2026-01-13 22:46:36.594102'),
('3dv927ipt4bim3vpperwz06jzpha5ua3', 'eyJjYXJ0Ijp7IjQiOjF9fQ:1vain3:u-c7lYBb0J8ioRYpMeFf9ZKwYCxSNO6X4fhCbHAqtoM', '2026-01-13 23:06:09.788311'),
('smym6dkcy41a7l7fkj3e74eng0srkjiz', 'eyJjYXJ0Ijp7IjMiOjF9fQ:1vajG5:TcCZhbDraia4NarMmYXt7nwPboEqPmwfno4XSm-soCI', '2026-01-13 23:36:09.068035'),
('afvu3gh2munphot9n41t4m4p2obgwxa0', 'eyJ3aXNobGlzdCI6WyI3Il19:1vbNJi:e0ThQ-ODgDjaDfJGoMSSLVRu0wWec44m0EELlcZo8jA', '2026-01-15 18:22:34.671433'),
('vibvk8h1rwx2odgs80uif7pjl5dxqzey', 'eyJjYXJ0Ijp7IjEwIjoxfX0:1vbNce:194XJNOdA9d5HJPpDea0iGs_BR-Lcecwii8dsBEamsU', '2026-01-15 18:42:08.898202'),
('p1oqtkba88rsdxha4x2qxkzt9gi1oqt6', 'eyJjYXJ0Ijp7IjYiOjF9fQ:1vbNlr:XXVYkphrBJhUB5PR5WN9bfUwLfyhP2M2wqXckbaV_2k', '2026-01-15 18:51:39.734446'),
('p7csxq3smotdisms3r8nkvku44xhd1me', 'eyJ3aXNobGlzdCI6WyI2Il19:1vbNvq:Xfs4DyW_a1S84Avp-wQ_0rDxzAEaazsnNemJw8IwbNY', '2026-01-15 19:01:58.273391'),
('zvksfo6aobpht2i4aymyokrxpajs253i', 'eyJ3aXNobGlzdCI6WyIxNCJdfQ:1vbOFW:hhgvqZcr2hqBn2q3nhI3xdv0ujiuI4b2pPj9blpmYVE', '2026-01-15 19:22:18.368107'),
('lm3x9pvfukk9zalo1gl4e419laf9594f', 'eyJjYXJ0Ijp7IjkiOjF9fQ:1vbOPa:br0pnJoVcb8kfoaMMJvXTX59gxjE0q3FtiJ-V2wS_9E', '2026-01-15 19:32:42.826257'),
('0p12r00txe59w072uxtjjy9oixw2y3z0', 'eyJ3aXNobGlzdCI6WyI5Il19:1vbPYm:ItMegQ2Lwe9FzkxDdSzrYXZ4HqgLjk-cnuq6SrT-Ahk', '2026-01-15 20:46:16.232733'),
('4duz9f1aw05dumvf2itic0rhhc3i4tnb', 'eyJ3aXNobGlzdCI6WyI3Il19:1vbPhY:_vXrCYEtESZx7LxKKaoXDghjrQXXf8fw_gILEIAwEyU', '2026-01-15 20:55:20.812836'),
('7bpcdgg1nu7ijvmx6gfha1pu0inzyy5b', 'eyJjYXJ0Ijp7IjYiOjF9fQ:1vbPrj:d0HklDgV923bYTl77jqicv57Wyx-SNCOBg45Zgc7bD8', '2026-01-15 21:05:51.314399'),
('zytea1q76omjaxzak74vsmzgf32ulvab', 'eyJjYXJ0Ijp7IjE2IjoxfX0:1vbQ1n:gJXPN3XuPPYtav4u1TkU6np2X2aqR0sLi_4Jty-Uw7Q', '2026-01-15 21:16:15.238879'),
('f00k62wjm51upy5am02m6su6bb6xzrd9', 'eyJjYXJ0Ijp7IjgiOjF9fQ:1vbQAl:ntK_d17t41AEHsNV3-w3zr8jNF-PXdxVTdHZXC9vuDk', '2026-01-15 21:25:31.124669'),
('0fxafsd5h078ff7r12j0jq7ogt0x43l0', 'eyJjYXJ0Ijp7IjkiOjF9fQ:1vbQJi:65buLEFV0gvAJe6sabD_TxaRDmlKHAryKEsebfGWnho', '2026-01-15 21:34:46.859204'),
('gp5mt51516k3c8kzpnq5g6v6eqsaok7d', 'eyJjYXJ0Ijp7IjEwIjoxfX0:1vbQUQ:CuvrMD4G9Oa2fG08eP0iNyNS-4bQ-PHMveFnqWPc96M', '2026-01-15 21:45:50.659620'),
('j28nnn5fk7ragrj1x37zgrw5oc415rix', 'eyJ3aXNobGlzdCI6WyI5Il19:1vbsrN:0B_KH-ciO2D1zvyOYomK3DIvvVDnvNjl6EeH8hPhK5s', '2026-01-17 04:03:25.243383'),
('o483kkm46k0not4rglq0w4fa7aj4zozq', 'eyJ3aXNobGlzdCI6WyI4Il19:1vc9ne:hJGkAmXMiDJjNuEMqSANm-WWqzq9ICtsFNseC6pYyBI', '2026-01-17 22:08:42.767133'),
('r6f0hgl45i60xqv7bsuf5w7cog625z50', 'eyJ3aXNobGlzdCI6WyIxMCJdfQ:1vc9yG:Abs_VP-M2sEiqVXy7eG89hO2BdAomHhqRFK9HUK83tw', '2026-01-17 22:19:40.245071'),
('uq0p98tfcpiwrrhbt93eaxavygn7yek0', 'eyJ3aXNobGlzdCI6WyIxMyJdfQ:1vcAZ2:WWZL95hcetoWpYLVp4318wFYWzANoWg19mOwXTMQzvo', '2026-01-17 22:57:40.277650'),
('mkp08mtcfxlw85sa8my6mvg12oztbkyf', 'eyJ3aXNobGlzdCI6WyIxNiJdfQ:1vcArw:YDZlQTKeoeWOiw0YmE2YKf7xtO4wVnOxxGzkCsZZzDg', '2026-01-17 23:17:12.075359'),
('o8mz73dyuntmjpusc0xw38w3ydr1uc8l', 'eyJjYXJ0Ijp7IjEiOjF9fQ:1vcSey:-vT_LC95f3W82IpP6j-IyMepG6VYf-R2eB3qY4EAdKI', '2026-01-18 18:17:00.150824'),
('2qprec1fg41u0491wvi9orubontvpdfj', 'eyJjYXJ0Ijp7IjEiOjF9fQ:1vcUxG:FwnU4Sck-bBK9Z3xPZ4pavWbW99SvhXUj6eAlfpysKo', '2026-01-18 20:44:02.353348'),
('igur065eznsvw8scccm3srp3vtev5gtf', 'eyJjYXJ0Ijp7IjE2IjoxfX0:1vd6Im:2m-_1D1DhAVgXMi348yWWIXUpaUyII0xs4ePytXpHww', '2026-01-20 12:36:44.943261'),
('w06sg2qrit932n46krralz6ucojuzggt', 'eyJ3aXNobGlzdCI6WyIxNiJdfQ:1vdC5x:7OmXV-WUxzph0YY-WuLRTThJ-9mKSXiMsC-wm-ddCu8', '2026-01-20 18:47:53.025981'),
('o0xc8534y4skq0m4h1ricnqa7qm230vm', 'eyJ3aXNobGlzdCI6WyIzIl19:1vdCPM:seTsJU58Tui63uV99zog3R6u6Qw3BwsrwH4leScClFA', '2026-01-20 19:07:56.586089'),
('g34kcmwngwdj3ids5ai4fwq2bq0t503y', 'eyJ3aXNobGlzdCI6WyIxIl19:1vdCj3:s919L2LwW9NslC-USE0Z3MSzndjTSDYEla45InGedWQ', '2026-01-20 19:28:17.597769'),
('ivdfucicl494342cj025k5h1hqmsvatl', 'eyJ3aXNobGlzdCI6WyIxMiJdfQ:1vdD2R:UsN3tojRIvFcgnRd_hm11GPKLm_-sNj4tJT9oKPv_zw', '2026-01-20 19:48:19.978123'),
('wwnxvl4rjv8466bpw1qi8bnrg3df3c9v', 'eyJ3aXNobGlzdCI6WyIxNSJdfQ:1vdDPy:7rfNQ_OS7BGFXn8Zqyq9dXObXNvBs0yOhUA4RqtOwF4', '2026-01-20 20:12:38.019911'),
('qkls3lnsz0odfeetc3u48rsenuda9p61', 'eyJjYXJ0Ijp7IjExIjoxfX0:1vdDV7:t1SPG5JFwhG2MzGDzMCIMbzpfE9FqVZKXNP40_FXMIw', '2026-01-20 20:17:57.806081'),
('nw200c1mmf4qeczqsvw38ssyroezk18f', 'eyJjYXJ0Ijp7IjMiOjF9fQ:1vdF3a:Kwq6FkE7n-45lKwPRVf64WOdPqrbX8Jvx6B_tj8ue4E', '2026-01-20 21:57:38.784892'),
('p9nzie90whd5bbkmgh5liloz6oiv2xf9', '.eJyrVkpOLCpRsqpWslCyMtRRsgSThoYQyghMGYNJEzBpCibNwKQ5RBGEYwiRMYQoMwTpqdVRKs8szsjJLAZaEA1SAZYHGQIyLrYWAHC-GoI:1vdThm:gZMNDzADl5rbNvrqqIKYsvk8GnqdOl5cWEn6qbWpCcg', '2026-01-21 13:36:06.710641'),
('7l4sxegltbcz7vtw1llf631uhq8pal3w', 'eyJ3aXNobGlzdCI6WyI5Il19:1vduwu:8DgwcE6aEjZX1YbXPVREVf-ko6_IFTJtFmgxnHBYBMU', '2026-01-22 18:41:32.898989'),
('cb0g3w83stxh2xxbifi145g978ax9m9s', 'eyJ3aXNobGlzdCI6WyI3Il19:1vdv5u:v0zkVFZQL-uTIKdHKduRD7vPUDxkZsaK9uW9fC5RSAc', '2026-01-22 18:50:50.330344'),
('qhtsbhh0nftu3pwzxs2cuapem0ti7y28', 'eyJjYXJ0Ijp7IjYiOjF9fQ:1vdvEz:JIRIoR-njaJxCaIt3Vf3rHvU2pqBIrXPG-MCEkeqH3g', '2026-01-22 19:00:13.776395'),
('21qp2snnz2ozbnlbq5ceh1rpfkcn0sfo', 'eyJjYXJ0Ijp7IjEwIjoxfX0:1vdvOq:h-5bbOlJccUdWoDN1X1pOt3tGXSvRqxG1gSseFpuDhg', '2026-01-22 19:10:24.707207'),
('l38t3fvh5czs1hvun6i9pta1w0gwpkmx', 'eyJjYXJ0Ijp7IjgiOjF9fQ:1vdvbh:RdousuuKZnONDVO3med0QXSxQMe1reVv8C8ajmk1GRo', '2026-01-22 19:23:41.062919'),
('qlphk6vm4gdh7oo9d609miqh6xze1ua1', 'eyJjYXJ0Ijp7IjkiOjF9fQ:1vdvhh:Y3BBAqpQB3Rr7WOWLMrVSxGvjXag81ftiPcBVUNsfdM', '2026-01-22 19:29:53.401875'),
('5vu9unt1lgd2om8yzs6678pyersng7n9', 'eyJjYXJ0Ijp7IjE2IjoxfX0:1vdvsN:a2to1u3uNOnShV7ZQrmxWDlUlkbGkOwnb6goWqPpVhI', '2026-01-22 19:40:55.112758'),
('ow39jb5pe2jiuh833nk937mezpa7vzlx', 'eyJ3aXNobGlzdCI6WyIxMCJdfQ:1vdzEX:tUIsyy_piI72uXp1nrwfWK8o53FZe6IjP8Vn6B370As', '2026-01-22 23:16:01.088483'),
('timmqqiks8ztl54l0hqcziert2qdyvwo', 'eyJjYXJ0Ijp7IjkiOjF9fQ:1vdzNe:3M61exENZnjXnc18zawVFWQXSmIBGtt0kEgvWfSEDP4', '2026-01-22 23:25:26.407004'),
('t0a3f7p0nt0a1xvsxm9bkeng0g4zms3n', 'eyJjYXJ0Ijp7IjYiOjF9fQ:1vdzhK:uTx1pnUyuGeCVtKw4zpryl8XwSQJ5eFJXxeDHVDGqgY', '2026-01-22 23:45:46.395808'),
('cupauuz6ffqxqpex65bb1s804v4pbjjo', 'eyJjYXJ0Ijp7IjEwIjoxfX0:1ve0Tf:45xRydJ7aA4R0P42QVAYfcLIwXUrtXTdDXueZs1e5jg', '2026-01-23 00:35:43.143851'),
('0eh9jcw4xrkr0pt3tqn5hprw8auekvq6', '.eJyrVkpOLCpRsqpWMlSyMtRRMgKTxmDSBEyagkkzIFlbCwD-0ApE:1ve3gD:JcWaXNpdGAqC8GqY8Q0akqNjdt3Y5Rfkz0m43Yy92yU', '2026-01-23 04:00:53.553512'),
('f00w7mw7t4r7o5bcv4nrytr2ksuuhmsi', '.eJxVjEEOwiAQRe_C2hAoQsGl-56BzDCMVA0kpV0Z765NutDtf-_9l4iwrSVuPS9xJnERWpx-N4T0yHUHdId6azK1ui4zyl2RB-1yapSf18P9OyjQy7f2Hh1ZTSaDReMtOD4DQ9bK2TAYpTiPbuCRtdUuUdDM3lhDAT2hYhTvD-h2ODo:1veDmY:ESduiZkdFm2e0GoDbLzc6R818vJ9zrtB6Hn7veMLBKo', '2026-01-23 14:48:06.445573'),
('zyoxibkc29inuh007mfz5wrqel7sn1ow', '.eJxVjEEOwiAQRe_C2hAoQsGl-56BzDCMVA0kpV0Z765NutDtf-_9l4iwrSVuPS9xJnERWpx-N4T0yHUHdId6azK1ui4zyl2RB-1yapSf18P9OyjQy7f2Hh1ZTSaDReMtOD4DQ9bK2TAYpTiPbuCRtdUuUdDM3lhDAT2hYhTvD-h2ODo:1veECn:5FtQ0zrGgY7KfjjZ_SR7dXlAFuCJ_0-VwH5t7q6kKlo', '2026-01-23 15:15:13.730663'),
('5bvavocgfcubblvxwqz3lludsgkqvvot', 'eyJjYXJ0Ijp7IjEzIjoxfX0:1veFis:lM_8rP0AYHPhqgqad5jS1tn1WdCTzCgYTId3imkg2KA', '2026-01-23 16:52:26.993983'),
('ya48tyacjyyqblkg3pmnf0km9dy4i09p', '.eJxVjEEOwiAQRe_C2hAoQsGl-56BzDCMVA0kpV0Z765NutDtf-_9l4iwrSVuPS9xJnERWpx-N4T0yHUHdId6azK1ui4zyl2RB-1yapSf18P9OyjQy7f2Hh1ZTSaDReMtOD4DQ9bK2TAYpTiPbuCRtdUuUdDM3lhDAT2hYhTvD-h2ODo:1veIid:24gy4nIcb_SjcPRnfZ-hRmemAxt2jqftVJBTtKS0wCc', '2026-01-23 20:04:23.812698'),
('9g0pkvafardmgfvyr2xh1w9wdhgvc4sa', 'eyJ3aXNobGlzdCI6WyIxMCJdfQ:1vecsn:a1ofbMPycPqQ5L2C95RVZAwvfkCZ82_BTIuLEG7Uwt8', '2026-01-24 17:36:13.286793'),
('si8jnw86y55ns8o7cuk3vmy5vfys44d0', 'eyJ3aXNobGlzdCI6WyI4Il19:1vedR0:_z9QduhD9W41hqY4p89i9L9EVFj70tiJfVkRbkSK7PU', '2026-01-24 18:11:34.902191'),
('7uwu5t3meru7sje4gbs9hpgg5clekmzy', 'eyJ3aXNobGlzdCI6WyIxNSJdfQ:1vedVk:z0JML9aekQMTmT59Dq8oEl2Tj_0wrQlqq6ZIv-VxQf8', '2026-01-24 18:16:28.030724'),
('gavgovrbup3h4qlakoogvi9395m8zyt4', 'eyJjYXJ0Ijp7IjEzIjoxfX0:1vedt9:TBeXeTcPtrKC-c3HGLahhGFktIla4orT6PoxcS1DwTY', '2026-01-24 18:40:39.788086'),
('18rt5gyeti37khgw3ze8b78zrxss9rl0', 'eyJ3aXNobGlzdCI6WyIxMyJdfQ:1vee8p:GT5ku4jA840U10rkfjRja_lvhxrOCzCcrB4ES5ytqoc', '2026-01-24 18:56:51.823445'),
('82wvkuj7c16ya5fxnzehmgwho4lqfjol', '.eJxVjEEOwiAQRe_C2hAoQsGl-56BzDCMVA0kpV0Z765NutDtf-_9l4iwrSVuPS9xJnERWpx-N4T0yHUHdId6azK1ui4zyl2RB-1yapSf18P9OyjQy7f2Hh1ZTSaDReMtOD4DQ9bK2TAYpTiPbuCRtdUuUdDM3lhDAT2hYhTvD-h2ODo:1vgODG:x_Oe3AmmgI7NeWwzmqjKpcG9V4d7PF2dnRCjgmm8Zbg', '2026-01-29 14:20:38.005810');

-- --------------------------------------------------------

--
-- Table structure for table `main_brand`
--

CREATE TABLE `main_brand` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `order` int(11) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `remark` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `main_brand`
--

INSERT INTO `main_brand` (`id`, `name`, `slug`, `is_active`, `order`, `created`, `updated`, `image`, `remark`) VALUES
(1, 'mriigg', 'mriigg', 1, 1, '2025-12-19 18:59:26.543754', '2025-12-19 18:59:26.543779', 'brands/2025/12/19/logo.webp', '<p>mriigg</p>'),
(2, 'Mod', 'mod', 1, 2, '2025-12-19 19:00:00.209359', '2025-12-19 19:00:00.209383', 'brands/2025/12/19/modlogo.webp', '<p>mod</p>'),
(3, 'Nykaa', 'nykaa', 1, 3, '2025-12-19 19:01:12.165100', '2025-12-19 19:01:12.165120', 'brands/2025/12/19/24clock.webp', '<p>sd</p>'),
(4, 'Nivea', 'nivea', 1, 4, '2025-12-19 19:02:19.712326', '2025-12-19 19:02:19.712360', 'brands/2025/12/19/Foundation.webp', '');

-- --------------------------------------------------------

--
-- Table structure for table `main_category`
--

CREATE TABLE `main_category` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `parent_id` bigint(20) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `order` int(11) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `main_category`
--

INSERT INTO `main_category` (`id`, `name`, `slug`, `parent_id`, `is_active`, `order`, `image`, `created`, `updated`) VALUES
(1, 'Makeup', 'makeup', NULL, 1, 1, 'categories/2025/12/19/mackup.webp', '2025-12-19 12:04:40.030453', '2025-12-19 12:04:40.030453'),
(2, 'Skin care', 'skin-care', NULL, 1, NULL, 'categories/2025/12/20/WhatsApp_Image_2025-12-07_at_10.37.58.webp', '2025-12-19 12:34:58.811860', '2025-12-22 16:16:37.486526'),
(3, 'Hair Care', 'hair-care', NULL, 1, NULL, 'categories/2025/12/20/WhatsApp_Image_2025-12-07_at_10.37.56.webp', '2025-12-19 12:54:37.026154', '2025-12-22 16:16:24.557974'),
(4, 'Heel Care', 'heel-care', NULL, 1, NULL, 'categories/2025/12/22/heel-care-cream.webp', '2025-12-22 17:06:36.766447', '2025-12-22 17:06:36.766478'),
(5, 'Face Care', 'face-care', NULL, 1, NULL, 'categories/2025/12/22/1.webp', '2025-12-22 17:07:23.376561', '2025-12-22 17:07:23.376589');

-- --------------------------------------------------------

--
-- Table structure for table `main_contactmessage`
--

CREATE TABLE `main_contactmessage` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `mobile` varchar(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  `message` longtext NOT NULL,
  `submitted_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `main_coupon`
--

CREATE TABLE `main_coupon` (
  `id` bigint(20) NOT NULL,
  `code` varchar(50) NOT NULL,
  `discount_amount` int(11) NOT NULL,
  `discount_type` varchar(10) NOT NULL,
  `min_purchase_amount` decimal(10,2) NOT NULL,
  `valid_from` datetime(6) NOT NULL,
  `valid_to` datetime(6) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `usage_limit` int(11) NOT NULL,
  `used_count` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `main_couponusage`
--

CREATE TABLE `main_couponusage` (
  `id` bigint(20) NOT NULL,
  `used_at` datetime(6) NOT NULL,
  `coupon_id` bigint(20) NOT NULL,
  `order_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `main_coupon_valid_categories`
--

CREATE TABLE `main_coupon_valid_categories` (
  `id` bigint(20) NOT NULL,
  `coupon_id` bigint(20) NOT NULL,
  `category_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `main_coupon_valid_products`
--

CREATE TABLE `main_coupon_valid_products` (
  `id` bigint(20) NOT NULL,
  `coupon_id` bigint(20) NOT NULL,
  `product_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `main_customuser`
--

CREATE TABLE `main_customuser` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) DEFAULT NULL,
  `last_name` varchar(150) DEFAULT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(254) NOT NULL,
  `mobile` varchar(15) NOT NULL,
  `role` varchar(20) NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `address_line1` varchar(255) DEFAULT NULL,
  `address_line2` varchar(255) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `zip_code` varchar(10) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `profile_image` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `main_customuser`
--

INSERT INTO `main_customuser` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `email`, `mobile`, `role`, `date_of_birth`, `gender`, `address_line1`, `address_line2`, `city`, `state`, `zip_code`, `country`, `profile_image`) VALUES
(1, 'pbkdf2_sha256$1000000$lCqQ7ICBWCjjkWnJUxmfj7$SXUeqY266SmC7MZnb43gU2oPNHkI/bcoFW9lHesbFMU=', '2026-01-15 14:20:38.000806', 1, 'mriiggadmin', NULL, NULL, 1, 1, '2025-12-29 12:06:13.413209', 'info@mriigg.com', '', 'customer', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, ''),
(2, 'pbkdf2_sha256$1000000$MKLMy8DUwfC4LDUBya0VdW$uC3bLyryVZ9qEw5j+FET3NMh6W39JEJKFSYaxag6V7U=', NULL, 0, 'user_817338', 'Swapnilshrivastava', '', 0, 1, '2026-01-10 10:29:43.310033', 'swapnilshrivastava794@gmail.com', '7987947020', 'customer', NULL, 'other', '', '', '', '', '', '', ''),
(3, 'pbkdf2_sha256$1000000$73bDKE6KLH5QV3d65vJxH8$DuXH/kJXcZo6aZQ3x9ZBVhqqNH3hkPIqsdgal5MCoHc=', NULL, 0, 'user_386735', 'Ankit', '', 0, 1, '2026-01-10 10:47:01.147736', 'dd@gmail.com', '5689568956', 'customer', NULL, 'other', '', '', '', '', '', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `main_customuser_groups`
--

CREATE TABLE `main_customuser_groups` (
  `id` bigint(20) NOT NULL,
  `customuser_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `main_customuser_user_permissions`
--

CREATE TABLE `main_customuser_user_permissions` (
  `id` bigint(20) NOT NULL,
  `customuser_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `main_order`
--

CREATE TABLE `main_order` (
  `id` bigint(20) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(254) NOT NULL,
  `address` varchar(250) NOT NULL,
  `postal_code` varchar(20) NOT NULL,
  `city` varchar(100) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `paid` tinyint(1) NOT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `discount_total` decimal(10,2) NOT NULL,
  `coupon_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `main_orderitem`
--

CREATE TABLE `main_orderitem` (
  `id` bigint(20) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `quantity` int(10) UNSIGNED NOT NULL,
  `order_id` bigint(20) NOT NULL,
  `product_id` bigint(20) NOT NULL,
  `variation_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `main_order_coupons`
--

CREATE TABLE `main_order_coupons` (
  `id` bigint(20) NOT NULL,
  `order_id` bigint(20) NOT NULL,
  `coupon_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `main_payment`
--

CREATE TABLE `main_payment` (
  `id` bigint(20) NOT NULL,
  `gokwik_oid` varchar(100) DEFAULT NULL,
  `transaction_id` varchar(100) DEFAULT NULL,
  `payment_method` varchar(50) DEFAULT NULL,
  `amount` decimal(10,2) NOT NULL,
  `status` varchar(20) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `response_data` longtext DEFAULT NULL,
  `order_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `main_product`
--

CREATE TABLE `main_product` (
  `id` bigint(20) NOT NULL,
  `name` varchar(200) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `available` tinyint(1) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `short_description` varchar(300) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `order` int(11) DEFAULT NULL,
  `featured` tinyint(1) NOT NULL,
  `latest` tinyint(1) NOT NULL,
  `offerprice` decimal(10,2) NOT NULL,
  `popular` tinyint(1) NOT NULL,
  `brand_id` bigint(20) DEFAULT NULL,
  `stock` int(10) UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Stock',
  `quantity` varchar(100) DEFAULT NULL COMMENT 'Qty',
  `unit` varchar(50) DEFAULT NULL COMMENT 'Unit',
  `is_sku_code` varchar(100) DEFAULT NULL COMMENT 'SKU Code',
  `color_code` varchar(7) DEFAULT NULL COMMENT 'Color Code',
  `subcategory_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `main_product`
--

INSERT INTO `main_product` (`id`, `name`, `slug`, `description`, `price`, `available`, `created`, `updated`, `short_description`, `is_active`, `order`, `featured`, `latest`, `offerprice`, `popular`, `brand_id`, `stock`, `quantity`, `unit`, `is_sku_code`, `color_code`, `subcategory_id`) VALUES
(1, 'Cosmetics Matte to Last Pore Blurring Loose Powder Banana 03 (10g)', 'cosmetics-matte-to-last-pore-blurring-loose-powder', '<p>Blur away pesky pores and unwanted shine to give your complexion a seamless, soft focus finish. Mriigg Matte To Last Pore Blurring Loose Powder comes with finely milled lightweight particles that feel super airy like but packs in a skin-smoothing punch. It sets your makeup in place for hours while soaking up sweat and oil instantly. Take your pick from 5 shades that are suited for all Indian skin tones, and one translucent shade.</p>', 500.00, 1, '2025-12-19 12:16:42.175658', '2025-12-19 12:16:42.175658', 'Blur away pesky pores and unwanted shine to give your complexion a seamless, soft focus finish.', 1, NULL, 1, 1, 450.00, 1, 1, 100, '100', 'g', 'PB100', '#ffb8b8', 1),
(2, 'MOD Daily Moisturizing Body Lotion with Licorice Deeply Hydrating and Lightening Lotion', 'mod-daily-moisturizing-body-lotion-with-licorice-d', '<p>Suitable for use on the entire body including face, MOD Moisturizing Lotion is especially designed with Licorice roots extracts that removes excess melanin, reduces dark spots and brightens the skin. It deeply nourishes the skin and provides 48 hours hydration. It deeply nourishes skin and boosts dull skin so that you get brighter and radiant skin look.</p>\r\n\r\n<p>&nbsp;</p>', 400.00, 1, '2025-12-19 12:38:14.810230', '2025-12-19 12:38:14.810258', 'MOD Daily Moisturizing Body Lotion', 1, NULL, 1, 1, 370.00, 1, 2, 100, '300', 'ml', 'DMLL-300', '#000000', 3),
(3, 'MOD Ghrit Kumari Hair Oil- hair growth with 100% Aloe Vera juice', 'mod-ghrit-kumari-hair-oil-hair-growth-with-100-alo', '<p>Ghrit Kumari hair oil infuses moisture into hair strands and strengthen hair roots so that you get<br />\r\nstrong, thick, soft, and shiny hair. It increases blood circulation and prevents itchiness of the scalp,<br />\r\nrepairs dead skin cells, and boosts new hair growth. Ghrit Kumari hair oil is made with 100% pure<br />\r\naloe vera juice which provides a protective layer, moisturizes hair strands, and deeply nourishes hair<br />\r\nroots. With very few applications of Ghrit Kumari hair oil, you will start noticing the wonderful results<br />\r\nin preventing hair fall and dandruff.</p>', 500.00, 1, '2025-12-19 13:03:36.026343', '2025-12-19 13:03:36.026363', 'MOD Ghrit Kumari Hair Oil- hair', 1, NULL, 1, 1, 470.00, 1, 2, 100, '300', 'ml', 'GKHO-300', '#000000', 4),
(4, 'MOD Onion Hair Oil with Fenugreek seed for hair repair, hair growth & strong hair', 'mod-onion-hair-oil-with-fenugreek-seed-for-hair-re', '<p>Made with 100% pure ingredients, MOD Onion Hair Oil a natural remedy for hair loss, hair thinning, poorly growing hair and powerless or dull hair.</p>\r\n\r\n<p>Onion Oil in combination with Fenugreek seed extracts helps in fast hair growth, strengthen hair roots, and reduces hair fall. It provides superior nourishment to the scalp and hair roots and increases blood circulation in hair roots. This oil works as a hair treatment therapy for damaged hair as it repairs, softens, and strengthens the dry and damaged hair.</p>\r\n\r\n<p>The restorative properties of the oil help to improve the texture of the hair damaged by pollutions or by the heat and chemicals of hairstyling products.?It helps in total repair, restore lustre and shine.</p>', 550.00, 1, '2025-12-19 13:07:04.610541', '2025-12-19 13:07:04.610571', 'Made with 100% pure ingredients, MOD Onion Hair Oil a natural remedy for hair loss, hair thinning, poorly growing hair and powerless or dull hair.', 1, NULL, 1, 1, 520.00, 1, 2, 100, '300', 'ml', 'OHO-300', '#000000', 4),
(5, 'MOD Onion Hair Shampoo with Fenugreek Chemical Free Hair Shampoo', 'mod-onion-hair-shampoo-with-fenugreek-chemical-fre', '<p>Made with 100% pure ingredients, MOD Onion Hair Shampoo is an exclusive formula that helps add strength into every strand.? The potent combination of Onion Juice and Fenugreek Seed in MOD Hair Shampoo works as a hair tonic which helps in hair repair &amp; recovery.</p>\r\n\r\n<p>Supplemented with Fenugreek Seed Extracts ? A Hair Tonic proven by scientists. It fights with hair loss issues and enables hair follicle to heal. This ?No Chemical Hair Shampoo? gives you thicker, fuller and healthier hair.</p>', 450.00, 1, '2025-12-19 13:10:52.473391', '2025-12-19 13:10:52.473414', '', 1, NULL, 1, 1, 420.00, 1, 2, 50, '300', 'ml', 'OHS-300', '#000000', 5),
(6, 'Too Faced Better Than Sex Liquid Eye Liner', 'too-faced-better-than-sex-liquid-eye-liner', '<p>A cutting-edge liquid eyeliner that&#39;s the easiest you&#39;ll ever use, created to produce a sharp, fluid, smudge-proof line every time. In one stroke, achieve an intense black line that lasts for 24 sexy hours. Combination of the Easy Glide 24-Hour waterproof formula and the innovative dual-fiber brush creates an eyeliner so amazing, it&#39;s ..Better Than Sex.</p>\r\n\r\n<p><strong>Reasons to Love:</strong></p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p>- Ultra rich deep black pigment</p>\r\n\r\n<p>- Intense pigment load (one swipe payoff)</p>\r\n\r\n<p>- Long-wearing for 24 hours</p>\r\n\r\n<p>- Waterproof and non-fading</p>\r\n\r\n<p>- Smudge proof</p>\r\n\r\n<p>- Flake proof</p>\r\n\r\n<p>- Free of parabens, phthalates and gluten</p>\r\n\r\n<p>- Too Faced is a cruelty-free brand</p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p><strong>Country of Origin:&nbsp;</strong>Belgium / Canada / Czech Republic / Dominican Republic / France / Germany / Italy / Japan / South Korea / Mexico / North Macedonia / Poland / Switzerland</p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p><strong>Generic Name:</strong>&nbsp;Makeup</p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p><strong>Name of Mfg / Brand:</strong>&nbsp;Estee Lauder Companies</p>\r\n\r\n<p><strong>Address of Mfg / Brand:</strong>&nbsp;the Estee Lauder Companies INC,767,fifth Avenue,New York,10153,United States of America</p>\r\n\r\n<p>&nbsp;</p>', 2500.00, 1, '2025-12-19 13:20:10.210942', '2025-12-19 13:20:10.210965', 'A cutting-edge liquid eyeliner that\'s the easiest you\'ll ever use, created to produce a sharp,', 1, NULL, 1, 1, 2390.00, 1, 3, 10, '0.6', 'ml', NULL, '#000000', 6),
(7, 'Too Faced Better Than Sex Mascara Travel Size - Black', 'too-faced-better-than-sex-mascara-travel-size-blac', '<p>Explore the entire range of Mascara available on Nykaa. Shop more Too Faced products here.You can browse through the complete world of Too Faced Mascara . Expiry Date: 15 January 2027 Country of Origin: Belgium Manufacturer: Estee Lauder Companies Address: the Estee Lauder Companies INC,767,fifth Avenue,New York,10153,United States of America Importer: ELCA Cosmetics Pvt. Ltd Address: 202-206 Tolstoy House,15 Tolstoy Marg, New Delhi 110001, India</p>', 1700.00, 1, '2025-12-19 13:26:11.744419', '2025-12-19 13:26:11.744440', 'Explore the entire range of Mascara available on Nykaa.', 1, NULL, 1, 1, 1550.00, 1, 3, 50, '4.8', 'g', 'nymsa-1Explore the entire range of Mascara available on Nykaa. Shop more Too Faced products here.You', '#000000', 6),
(8, 'Nykaa Skin Makeup Melter Cleansing Balm – Removes Waterproof Makeup, Excess Oil & Unclogs Pores', 'nykaa-skin-makeup-melter-cleansing-balm-removes-wa', '<p><strong>Nykaa Skin Makeup Melter Cleansing Balm:&nbsp;</strong>Removes Waterproof Makeup, Excess Oil &amp; Clogged Pore.</p>\r\n\r\n<p>Melt the day away with the Nykaa Collection Makeup Melter Cleansing Balm. This buttery-soft balm glides on smoothly, dissolving long-wear makeup, dirt, oil, and impurities in seconds. Enriched with Skin loving Ingredients. it leaves your skin feeling cleansed, soft, and comforted - never stripped. All in a fun, twist-easy jar you&rsquo;ll love reaching for.</p>\r\n\r\n<p><strong>Why you&#39;ll love it:&nbsp;</strong></p>\r\n\r\n<ul>\r\n	<li>Instant Melt, Effortless Cleanse</li>\r\n	<li>Melts waterproof makeup in seconds</li>\r\n	<li>Deep cleanses excess oil, dirt &amp; impurtities&nbsp;</li>\r\n	<li>Removes excess oil &amp; unclogs pores</li>\r\n	<li>Smart grinding jar for easy &amp; hygienic use.</li>\r\n</ul>\r\n\r\n<p><strong>Formulated with skin loving ingredients.&nbsp;</strong></p>\r\n\r\n<ul>\r\n	<li>Safflower seed oil - helps dissolve makeup without drying skin</li>\r\n	<li><strong>Cica:&nbsp;</strong>Strengthens the skin barrier &amp; soothes irritation</li>\r\n	<li>Vitamin E - moisturises skin to prevent dryness.</li>\r\n</ul>\r\n\r\n<p><br />\r\n&nbsp;</p>\r\n\r\n<p>Explore the entire range of&nbsp;<a href=\"https://www.nykaa.com/skin/cleansers/cleansing-oils-balm/c/25745?ptype=lst&amp;id=25745\" target=\"_blank\"><u>Cleansing Oils &amp; Balm</u></a>&nbsp;available on Nykaa. Shop more&nbsp;<a href=\"https://www.nykaa.com/brands/nykaa-skin/c/74554?ptype=brand&amp;id=74554\" target=\"_blank\"><u>Nykaa Skin</u></a>&nbsp;products here.You can browse through the complete world of&nbsp;<a href=\"https://www.nykaa.com/brands/nykaa-skin/c/74554?ptype=brand&amp;id=74554&amp;category_filter=25745&amp;sort=popularity\" target=\"_blank\"><u>Nykaa Skin Cleansing Oils &amp; Balm&nbsp;</u></a>.</p>\r\n\r\n<p>Expiry Date: 15 August 2027</p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p>Country of Origin: &nbsp;&nbsp;</p>\r\n\r\n<p>India</p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p>Manufacturer: &nbsp;&nbsp;</p>\r\n\r\n<p>N. G. ELECTRO PRODUCTS PRIVATE LIMITED</p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p>Address: &nbsp;&nbsp;</p>\r\n\r\n<p>NG Electro Products Pvt. Ltd., Unit II Plot No. 36, HIMUDA Industrial Area Phase IV, Bhatolikalan, Baddi Distt. Solan, (H.P) - 173205, Mfg. Lic. No. HIM/COS/18/266 Made In India.</p>\r\n\r\n<p>&nbsp;</p>', 750.00, 1, '2025-12-19 17:02:41.800914', '2025-12-19 17:02:41.800940', 'Nykaa Skin Makeup Melter Cleansing Balm: Removes Waterproof Makeup, Excess Oil & Clogged Pore.', 1, NULL, 1, 1, 699.00, 1, 3, 60, '350', 'ml', 'Nyfac-2', '#000000', 7),
(9, 'NYX Professional Makeup Bare With Me Serum And Calm Concealer - Beige', 'nyx-professional-makeup-bare-with-me-serum-and-cal', '<p>Explore the entire range of Concealer available on Nykaa. Shop more NYX Professional Makeup products here.You can browse through the complete world of NYX Professional Makeup Concealer . Expiry Date: 15 February 2028 Country of Origin: South Korea</p>', 999.00, 1, '2025-12-19 17:10:16.384330', '2025-12-24 17:40:08.681563', 'Explore the entire range of Concealer available on Nykaa.', 1, NULL, 1, 1, 949.00, 1, 3, 50, '9.6', 'ml', 'nyfac-3', '#000000', 7),
(10, 'NYX Professional Makeup Buttermelt Glaze Soft Glow Skin Tint + SPF 30 - Cashew Butta', 'nyx-professional-makeup-buttermelt-glaze-soft-glow', '<p>Butta glaze, butta care, butta shield; there is nothin&#39; butta than this triple threat!Get an instant glowing, glazed skin look with Buttermelt Glaze Soft Glow Skin Tint. A skin tint formula that is butta than the rest! Our Buttermelt Glaze Soft Glow Skin Tint with SPF melts right in for butta glazed skin. Go from skin that&#39;s lookin&#39; dull to skin that&#39;s givin&#39; GLAZE and a hydrated appearance! Get glazed donut skin + SPF 30 protection in a skincare-based formula that wears for up to 12 hours.Packed with Skin Nourishing Skincare Ingredients: Infused with Shea Butter, Mango Butter, &amp; Niacinamide, you&#39;ll be lookin&#39; butta than ever with this 93% skincare formula. This non greasy glaze leaves skin smooth and protected with a glowy skin tint!Skin Tint with SPF 30: Achieve a soft (and protected!) glowing all-day glazed look with Buttermelt Glaze Skin Tint&#39;s fade resist, no white cast formula. With broad-spectrum SPF 30, this nourishing skin tint also helps to shield skin against harmful UVA and UVB rays!</p>\r\n\r\n<p><strong>Features:</strong></p>\r\n\r\n<ul>\r\n	<li>Provides a natural, no-makeup makeup look for upto 12H</li>\r\n	<li>Skin tint infused with Shea Butter, Mango Butter, and Niacinamide.</li>\r\n	<li>Lightweight, moisturizing, and comfortable on the skin with broad spectrum SPF 30 protection</li>\r\n	<li>Resistant to fading, creasing, and transfer.</li>\r\n</ul>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p><strong>About the Brand:</strong>&nbsp;Born in 1999, NYX Professional Makeup is a pro makeup brand embraces diversity and beauty with cruelty-free and vegan makeup products and absolutely no retouched pictures!AT NYX PROFESSIONAL MAKEUP, WE ALWAYS WANT TO BE THE BRIGHTEST PART OF YOUR DAY!We pledge to be on the right (or should we say BRIGHT) side of positivechange in our world and the people within it, while always committing to the best quality products.</p>\r\n\r\n<p>&nbsp;</p>', 1450.00, 1, '2025-12-19 17:19:15.712134', '2025-12-19 17:28:30.086300', 'Butta glaze, butta care, butta shield; there is nothin\' butta than this triple threat!Get an instant glowing, glazed skin look with Buttermelt Glaze Soft Glow Skin Tint. A skin tint formula that is butta than the rest!', 1, NULL, 1, 1, 1305.00, 1, 3, 50, '30', 'ml', 'nyfac-4', '#000000', 7),
(11, 'Nykaa Naturals Tea Tree & Neem Purifying & Hydrating Gel - Controls Oils, Acne & Uneven tone Skin', 'nykaa-naturals-tea-tree-neem-purifying-hydrating-g', '<p>Nykaa Naturals Lavender &amp; Chamomile Calming Gel &amp; Tea Tree &amp; Neem Purifying Gel</p>\r\n\r\n<p>Nykaa Naturals Hydrating Gel replenishes your skin with a boost of hydration that lasts all day long. The lightweight texture of the gel gets instantly absorbed into your skin to leave it plump, dewy and nourished. Choose from 2 different variants that go beyond hydration to address common skin concerns.</p>\r\n\r\n<p><strong>TOP FEATURES:</strong></p>\r\n\r\n<ul>\r\n	<li>Gel based moisturizer that hydrates &amp; nourishes the skin</li>\r\n	<li>Lightweight, non-sticky formula that gets absorbed easily</li>\r\n	<li>Enriched with active ingredients that give a boost of hydration</li>\r\n	<li>Suitable for all skin types</li>\r\n</ul>\r\n\r\n<p>2 TYPES FOR COMMON SKIN CONCERNS</p>\r\n\r\n<p>TEA TREE AND NEEM - PURIFYING</p>\r\n\r\n<p>TEA TREE</p>\r\n\r\n<p>Anti-microbial properties that treat acne</p>\r\n\r\n<p><strong>NEEM</strong></p>\r\n\r\n<p>Treats uneven skin tone &amp; controls oil production</p>\r\n\r\n<p>LAVENDER AND CHAMOMILE - CALMING</p>\r\n\r\n<p>LAVENDER</p>\r\n\r\n<p>Antifungal properties that heal breakouts &amp; inflammations</p>\r\n\r\n<p><strong>CHAMOMILE&nbsp;</strong></p>\r\n\r\n<p>Reduces redness, irritation &amp; calms skin</p>\r\n\r\n<p><strong>ACTIVE INGREDIENTS</strong></p>\r\n\r\n<p>Aloe Vera Extract</p>\r\n\r\n<p>Soothes sun burns, deeply moisturizes and fights skin ageing</p>\r\n\r\n<p><strong>Cucumber Extract&nbsp;</strong></p>\r\n\r\n<p>Reduces puffiness, rejuvenates skin and reduces dark circles</p>\r\n\r\n<p><strong>Rose Water</strong></p>\r\n\r\n<p>Acts as a toner, lightens skin pigmentation and hydrates skin</p>\r\n\r\n<p><strong>HOW TO USE</strong></p>\r\n\r\n<p><strong>STEP 1</strong></p>\r\n\r\n<ul>\r\n	<li>Scoop out a small amount of gel and dot it on your face and neck</li>\r\n</ul>\r\n\r\n<p><strong>STEP 2</strong></p>\r\n\r\n<ul>\r\n	<li>Gently massage the gel in an upward motion</li>\r\n</ul>\r\n\r\n<p><strong>STEP3</strong></p>\r\n\r\n<ul>\r\n	<li>Use daily to keep your skin hydrated all day</li>\r\n</ul>\r\n\r\n<p><strong>WEEKLY REGIME FOR HYDRATED SKIN</strong></p>\r\n\r\n<p><strong>CLEANSE</strong></p>\r\n\r\n<ul>\r\n	<li>Wash your skin with the Nykaa Naturals Face Wash that rids your skin of impurities and makeup residue.</li>\r\n</ul>\r\n\r\n<p><strong>EXFOLIATE</strong></p>\r\n\r\n<ul>\r\n	<li>Deep cleanse your skin with Nykaa Naturals Face Scrub that unclogs pores and removes oil build-up.</li>\r\n</ul>\r\n\r\n<p><strong>HYDRATE</strong></p>\r\n\r\n<ul>\r\n	<li>Give your skin a boost of hydration with Nykaa Naturals Hydrating Gel that retains moisture to keep your skin soft and nourished.</li>\r\n</ul>\r\n\r\n<p><strong>NOURISH</strong></p>\r\n\r\n<ul>\r\n	<li>Replenish &amp; rejuvenate your skin with Nykaa Naturals Facial Oils that&#39;s suitable for all skin types &amp; concerns.</li>\r\n</ul>\r\n\r\n<ul>\r\n	<li>CLAIMS</li>\r\n	<li>PARABEN FREE</li>\r\n	<li>No animal testing</li>\r\n	<li>MINERAL OIL FREE</li>\r\n</ul>', 349.00, 1, '2025-12-22 17:41:09.060537', '2025-12-22 17:41:09.060554', 'Nykaa Naturals Lavender & Chamomile Calming Gel & Tea Tree & Neem Purifying Gel', 1, NULL, 1, 1, 149.00, 1, 3, 30, '100', 'g', 'nyfac-5', '#000000', 11),
(12, 'Nykaa Naturals Tea Tree Essential Oil For Acne & Hair Fall Control Solution - 100% Natural', 'nykaa-naturals-tea-tree-essential-oil-for-acne-hai', '<p>Explore the entire range of Face Oils available on Nykaa. Shop more Nykaa Skin products here.You can browse through the complete world of Nykaa Skin Face Oils .</p>', 350.00, 1, '2025-12-22 17:51:50.635991', '2025-12-22 17:51:50.636010', 'Explore the entire range of Face Oils available on Nykaa.', 1, NULL, 1, 1, 245.00, 1, 3, 50, '10', 'ml', 'nyhairoil-2', '#000000', 4),
(13, 'Nykaa Naturals Jojoba 100% Pure Cold Pressed Face Oil-Deep Hydration & Nourishment - All Skin Types', 'nykaa-naturals-jojoba-100-pure-cold-pressed-face-o', '<p>Explore the entire range of Face Oils available on Nykaa. Shop more Nykaa Skin products here.You can browse through the complete world of Nykaa Skin Face Oils . Expiry Date: 15 January 2028</p>', 500.00, 1, '2025-12-22 18:00:40.116982', '2025-12-22 18:00:40.117005', 'Explore the entire range of Face Oils available on Nykaa.', 1, NULL, 1, 1, 300.00, 1, 3, 50, '30', 'ml', 'nyoil-3', '#000000', 20),
(14, 'Nyassa Under The Ocean Rejuvenating Bath Salts', 'nyassa-under-the-ocean-rejuvenating-bath-salts', '<p>Under the Ocean bath salt is a combination of two highly beneficial salts &ndash; sea salt and espon salt. While sea salt has been shown to improve muscle cramps, espon salt comes with a wide range of benefits that soothe the body and the mind. It is a natural healing agent, curing skin problems and easing back pain and body aches. It is also a good exfoliant, removing blackheads along with dead skin.</p>\r\n\r\n<p><strong>Additional Information:</strong>&nbsp;Nyassa creates unique bath and body products from the finest of natural ingredients, to blend that with some of the most exotic fragrances, they offer a wide range of diverse products, to constantly innovate and diligently research, to understand the myriad ways in which hundreds of nutritious and efficacious natural ingredients work, to learn and to apply that knowledge on how it works on various skin types, to intelligently differentiate the appropriate ingredients of a face cream from that of a face wash, and hence formulate each, to keep up to the ever changing expectations of the consumers, delivering value and changing ordinary everyday experiences.</p>', 400.00, 1, '2025-12-22 18:13:17.774776', '2025-12-22 18:13:17.774802', 'Under the Ocean bath salt is a combination of two highly beneficial salts – sea salt and espon salt.', 1, NULL, 1, 1, 360.00, 1, 3, 50, '220', 'g', 'nyksal-2', '#000000', 32),
(15, 'Nyassa Under The Ocean Hand And Body Moisturizer', 'nyassa-under-the-ocean-hand-and-body-moisturizer', '<p>Organic cold-pressed sweet almond oil, rich in Vitamin A and Vitamin E, provides deep moisturization that helps keep your skin healthy and glowing while preventing dryness and flakiness.Shea butter offers rich, long-lasting hydration as a natural moisturizer, helps maintain smooth and supple skin, provides a mild sun protection factor with its natural compounds, and is high in Vitamin A and Vitamin E, which support skin health and enhance its natural radiance.The Aqua fragrance leaves a lingering, delicate scent that soothes and uplifts your senses, adding a touch of elegance and relaxation to your skincare routine.The gentle formula is suitable for all skin types, including sensitive skin, and absorbs quickly without leaving any oily residue.Natural and Safe: Free from Harmful Chemicals: No parabens, sulfates, or artificial additives.</p>\r\n\r\n<p><strong>Features:</strong></p>\r\n\r\n<ul>\r\n	<li><strong>Organic Cold-Pressed Sweet Almond Oil:</strong>&nbsp;Rich in Vitamin A and E, it deeply moisturizes and keeps skin glowing while preventing dryness and flakiness.</li>\r\n	<li><strong>Shea Butter:</strong>&nbsp;Provides long-lasting hydration and a mild sun protection factor, enhancing skin smoothness and radiance with its high Vitamin A and E content.</li>\r\n	<li><strong>Supports Skin Freshness:</strong>&nbsp;Maintains skin vitality and radiance by promoting the formation of new skin cells.</li>\r\n</ul>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p><strong>About the Brand:</strong>&nbsp;Since 2007 Nyassa has been creating unique bath and body products from the finest of natural ingredients available in the world. Blending that with some of the most exotic fragrances, Nyassa offers a wide range of diverse products. It&rsquo;s a constant endeavor to innovate and diligently research, to understand the myriad ways, in which hundreds of nutritious and efficacious natural ingredients work, to learn and to apply that knowledge on how it works on various skin types. To top it all we naturally differentiate the appropriate ingredients to keep up to the ever changing expectations of the consumers, delivering value and changing ordinary everyday experiences. You know it&rsquo;s Nyassa when you inhale the exotic fragrance that accompanies all its products.</p>\r\n\r\n<p>&nbsp;</p>', 599.00, 1, '2025-12-22 18:21:38.556657', '2025-12-22 18:21:38.556677', 'Organic cold-pressed sweet almond oil, rich in Vitamin A and Vitamin E, provides deep moisturization that helps keep your skin healthy and glowing while preventing dryness and flakiness.', 1, NULL, 1, 1, 539.00, 1, 3, 100, '200', 'ml', 'Nykaa-33', '#000000', 3),
(16, 'Nykaa SkinRX Ceramide Barrier Repair Face Moisturizer with SPF 15- All Skin Types', 'nykaa-skinrx-ceramide-barrier-repair-face-moisturi', '<p>Nykaa SkinRX Ceramide Barrier Repair Face Moisturizer with SPF 15- All Skin Types: Explore the entire range of Face Moisturizer &amp; Day Cream available on Nykaa. Shop more Nykaa Skin products here.You can browse through the complete world of Nykaa Skin Face Moisturizer &amp; Day Cream . Expiry Date: 15 October 2026</p>', 399.00, 1, '2025-12-22 18:32:18.659643', '2025-12-22 18:32:18.659662', 'Nykaa SkinRX Ceramide Barrier Repair Face Moisturizer with SPF 15- All Skin Types: Explore the entire range of Face Moisturizer & Day Cream available on Nykaa.', 1, NULL, 1, 1, 239.00, 1, 3, 99, '50', 'g', 'nyfac-9', '#000000', 11);

-- --------------------------------------------------------

--
-- Table structure for table `main_productdetailsection`
--

CREATE TABLE `main_productdetailsection` (
  `id` bigint(20) NOT NULL,
  `title` varchar(200) NOT NULL,
  `content` longtext NOT NULL,
  `product_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `main_productdetailsection`
--

INSERT INTO `main_productdetailsection` (`id`, `title`, `content`, `product_id`) VALUES
(1, 'Product detail sections', '<p>Blur away pesky pores and unwanted shine to give your complexion a seamless, soft focus finish. Nykaa Matte To Last Pore Blurring Loose Powder comes with finely milled lightweight particles that feel super airy like but packs in a skin-smoothing punch. It sets your makeup in place for hours while soaking up sweat and oil instantly. Take your pick from 5 shades that are suited for all Indian skin tones, and one translucent shade.<br />\r\n<br />\r\n&nbsp;</p>\r\n\r\n<p>Explore the entire range of&nbsp;<a href=\"https://www.nykaa.com/makeup/face/loose-powder/c/229?ptype=lst&amp;id=229\" target=\"_blank\"><u>Loose Powder</u></a>&nbsp;available on Nykaa. Shop more&nbsp;<a href=\"https://www.nykaa.com/brands/nykaa-cosmetics/c/1937?ptype=brand&amp;id=1937\" target=\"_blank\"><u>Nykaa Cosmetics</u></a>&nbsp;products here.You can browse through the complete world of&nbsp;<a href=\"https://www.nykaa.com/brands/nykaa-cosmetics/c/1937?ptype=brand&amp;id=1937&amp;category_filter=229&amp;sort=popularity\" target=\"_blank\"><u>Nykaa Cosmetics Loose Powder&nbsp;</u></a>.</p>\r\n\r\n<p>Expiry Date: 15 May 2</p>', 1),
(2, 'Key Points:', '<ul>\r\n	<li>Contains Licorice Root Extracts which is excellent for skin lightening and anti-ageing effects</li>\r\n	<li>Keeps skin hydrated and moisturized for 48 hours</li>\r\n	<li>Fade dark spots and improve hyperpigmentation</li>\r\n	<li>Prevents skin pigmentation and sun damage from UVB rays</li>\r\n	<li>Strengthen skin?s defence against harmful rays</li>\r\n</ul>', 2),
(3, 'Point', '<p>Made with pure Aloe Vera Juice</p>\r\n\r\n<ul>\r\n	<li>Boosts new hair growth</li>\r\n	<li>Gives strong, shiny, and thick hair</li>\r\n	<li>Stops hair fall and dandruff</li>\r\n	<li>Moisturises hair strands and nourishes hair roots</li>\r\n</ul>\r\n\r\n<ul>\r\n	<li>&nbsp;</li>\r\n</ul>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p>&nbsp;</p>', 3),
(4, 'Key Points:', '<ul>\r\n	<li>Potent combination of Onion Oil and Fenugreek Seeds extract</li>\r\n	<li>Restore lustre &amp; shine</li>\r\n	<li>Boosts Hair Growth</li>\r\n	<li>Adds Strength &amp; Shine</li>\r\n	<li>Nourishes Scalp</li>\r\n	<li>No chemicals&amp; toxins, No paraben</li>\r\n</ul>', 4),
(5, 'Key Points:', '<ul>\r\n	<li>Contains no chemicals, no sulphate, no paraben</li>\r\n	<li>Formulated with 100% Pure Onion Juice and Fenugreek Seed Extracts</li>\r\n	<li>Onion Juice and Fenugreek Seed works as the best tonic for hair</li>\r\n	<li>Gives Thicker, Fuller and Healthier hair</li>\r\n	<li>Works as hair tonic and helps in hair repair and recovery</li>\r\n	<li>Prevents dandruff and hair fall</li>\r\n</ul>\r\n\r\n<ul>\r\n	<li>&nbsp;</li>\r\n</ul>\r\n\r\n<form action=\"https://modwellness.in/shop/hair-shampoo/mod-onion-hair-shampoo-with-fenugreek-chemical-free-hair-shampoo/\" enctype=\"multipart/form-data\" method=\"post\">&nbsp;</form>\r\n\r\n<p>&nbsp;</p>', 5),
(6, 'Ingredients', '<p>Water, Butylene Glycol, Acrylates/Ethylhexyl Acrylate Copolymer, Alcohol, Beheneth-30, Phenoxyethanol, Laureth-21, Aminomethyl Propanol, Black 2 (CI 77266).</p>\r\n\r\n<p>Please be aware that ingredient lists may change or vary from time to time. Please refer to the ingredient list on the product package you receive for the most up to date list of ingredients.</p>', 6),
(7, 'How To Use', '<p>Shake before applying! Lay brush down against lashline and allow the flexible bristles to hug lash line for the perfect tight line. Use the precision tip to flick up and out.</p>\r\n\r\n<p>&nbsp;</p>', 6),
(8, 'Ingredients', '<p>Aqua/Water/Eau, Synthetic Beeswax, Paraffin, Glyceryl Stearate, Acacia Senegal Gum, Butylene Glycol, Oryza Sativa (Rice) Bran Wax/Oryza Sativa Bran Cera, Stearic Acid, Palmitic Acid, Polybutene, VP/Eicosene Copolymer, Copernicia Cerifera (Carnauba) Wax/Copernicia Cerifera Cera/Cire De Carnauba, Aminomethyl Propanol, Glycerin, PVP, Ethylhexylglycerin, Hydroxyethylcellulose, Disodium EDTA, Polyester-11, Cellulose, Trimethylpentanediol/Adipic Acid/Glycerin Crosspolymer, Propylene Glycol, Disodium Phosphate, Polysorbate 60, Acacia Seyal Gum Extract, Sodium Phosphate, Acetyl Hexapeptide-1, Dextran, Phenoxyethanol, Potassium Sorbate, Iron Oxides (CI 77499), Ultramarines (CI 77007), Black 2 (CI 77266).</p>\r\n\r\n<p>Please be aware that ingredient lists may change or vary from time to time. Please refer to the ingredient list on the product package you receive for the most up to date list of ingredients.</p>', 7),
(9, 'How To Use', '<p><strong>Suggested usage:</strong></p>\r\n\r\n<ul>\r\n	<li>Apply from base to tip for luscious, volumized lashes.</li>\r\n	<li>One coat and lashes are full and defined.</li>\r\n	<li>Two coats and lashes are even more luscious, curled, and dramatic.</li>\r\n	<li>Three coats help you achieve the most intense, black, multidimensional lashes possible.</li>\r\n</ul>', 7),
(10, 'How To Use', '<ul>\r\n	<li>Remove the lid from the grinder packaging.</li>\r\n	<li>Twist or rotate the grinder mechanism to release a small amountof the balm.</li>\r\n	<li>Use clean, dry fingers or a spatula to scoop up the dispensed balm. Massage the balm onto your dry face in circular motions.</li>\r\n	<li>Use lukewarm water to rinse off the balm.</li>\r\n	<li>Pat your skin dry with a clean towel.</li>\r\n</ul>', 8),
(11, 'Ingredients', '<ul>\r\n	<li>Remove the lid from the grinder packaging.</li>\r\n	<li>Twist or rotate the grinder mechanism to release a small amountof the balm.</li>\r\n	<li>Use clean, dry fingers or a spatula to scoop up the dispensed balm. Massage the balm onto your dry face in circular motions.</li>\r\n	<li>Use lukewarm water to rinse off the balm.</li>\r\n	<li>Pat your skin dry with a clean towel.</li>\r\n</ul>', 8),
(12, 'Ingredients', '<p><strong>Key Ingredients:</strong>&nbsp;This water-based liquid concealer is packed with skin-loving ingredients like tremella mushroom, cica (also known as centella asiatica) extract and green tea. It&rsquo;s hydrating and suitable for all skin types, especially those with dry, sensitive, or stressed skin.</p>', 9),
(13, 'How To Use', '<p>After prepping your skin with primer, dispense one pump of Bare With Me Concealer Serum onto a blending brush, such as Bare With Me Skin Serum Brush, and blend evenly over the skin. For problem areas, like dry under eyes, blotchy patches, or blemishes, use two pumps for medium coverage that lasts all day.</p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p><strong>Pro Tip:</strong>&nbsp;Finish with a few spritzes of the Bare With Me Multitasking Spray, which primes, sets, and refreshes makeup.</p>', 9),
(14, 'Ingredients', '<p>Aqua / Water / Eau , Glycerin , Homosalate , Octocrylene , Ci 77891 / Titanium Dioxide , Caprylyl Methicone , Ethylhexyl Salicylate , Dimethicone , Silica , Butyloctyl Salicylate , Cetyl Peg/Ppg-10/1 Dimethicone , Niacinamide , Propanediol , Dimethicone/Peg-10/15 Crosspolymer , Phenoxyethanol , Sodium Chloride , Synthetic Fluorphlogopite , Trimethylsiloxysilicate , Disteardimonium Hectorite , Ci 77492 / Iron Oxides , Chlorphenesin , Caprylyl Glycol , Disodium Stearoyl Glutamate , Silica Silylate , Trisodium Ethylenediamine Disuccinate , Mangifera Indica Seed Butter / Mango Seed Butter , Butyrospermum Parkii Butter / Shea Butter , Ci 77491 / Iron Oxides , Simethicone , Parfum / Fragrance , Maltodextrin , Adenosine , Aluminum Hydroxide , Dipropylene Glycol , Sodium Hyaluronate , Citric Acid , Sodium Citrate , Ci 77499 / Iron Oxides , Camellia Sinensis Leaf Extract , Tocopherol , Limonene , Pentaerythrityl Tetra-Di-T-Butyl Hydroxyhydrocinnamate</p>\r\n\r\n<p><strong>Key Ingredients:&nbsp;</strong>Shea Butter, Mango Butter, Niacinamide</p>', 10),
(15, 'How To Use', '<p>Get ready to glaze it up! Shake well and apply onto skin with fingers, a makeup sponge, or brush. Watch as the formula melts right in for healthy and even skin tone</p>\r\n\r\n<p>&nbsp;</p>', 10),
(16, 'How To Use', '<p>Tea Tree oil can be used with coconut oil, olive oil, and almond carrier oils.</p>\r\n\r\n<ul>\r\n	<li><strong>Skin:&nbsp;</strong>Add 3 to 4 drops in almond oil to soothe dry skin leave it on overnight to see best results. Simply add a few drops to a mixture of yogurt and honey for skin-brightening effects. Combine with shea butter or coconut oil to create salves to treat infections.</li>\r\n	<li><strong>Hair:&nbsp;</strong>Mix equal parts with coconut oil and massage into the scalp before rinsing it thoroughly to soothe the scalp and treat dandruff. Mix with a light carrier oil like almond oil and use as a serum. Add a few drops in your regular hair care products to enhance their therapeutic properties.</li>\r\n	<li><strong>Massage:&nbsp;</strong>Ease out the stress in your mind while loosening up tired muscles. Mix 5 drops in 10ml of base oil for massage.</li>\r\n	<li><strong>Aromatherapy:&nbsp;</strong>Diffused aromatically; drop 5-8 drops in a diffuser burner or vaporizer. It will give off a pleasurable aroma creating a pleasant atmosphere on any occasion, disinfecting the air of unwanted odors and some airborne pathogens.&nbsp;</li>\r\n	<li><strong>Natural Deodorizer:&nbsp;</strong>Combine with Shea Butter and Coconut Oil or Beeswax and pour into a roll-on bottle to make a natural deodorant.</li>\r\n	<li><strong>Repel insects and soothe insect bites:&nbsp;</strong>Combine 3-4 drops of tea tree oil with water for a DIY insect repellent solution.</li>\r\n</ul>\r\n\r\n<p><strong>Caution:</strong></p>\r\n\r\n<ul>\r\n	<li>Essential oils should always be applied after diluting with carrier oils/lotion or as mentioned in the directions to use.</li>\r\n	<li>The oils come with a leaflet with details of How to use, for more details, you can also contact our beauty experts online.</li>\r\n	<li>If applying an essential oil to your skin always perform a small patch test (after you have properly diluted the oil in an appropriate carrier.</li>\r\n	<li>For external use only.</li>\r\n	<li>Keep out of the reach of children.</li>\r\n	<li>Avoid contact with eyes.</li>\r\n</ul>\r\n\r\n<p>&nbsp;</p>', 12),
(17, 'How To Use', '<ul>\r\n	<li><strong>For sunburn:</strong>&nbsp;Apply 1-2 drops on affected area to ease sunburn and redness.</li>\r\n	<li><strong>For face:</strong>&nbsp;Apply 2-3 drops on your face and massage to control sebum and regulate oily skin.</li>\r\n	<li><strong>Scalp and hair care:</strong>&nbsp;For moisturized, clean scalp and reduced hair fall, massage regularly on your scalp after mixing a few drops with coconut oil.</li>\r\n	<li><strong>Hair care:</strong>&nbsp;Maintain your hair color by applying a few drops on your hair before going for a swim or a bath.</li>\r\n	<li><strong>Shaving cream:</strong>&nbsp;Use as a substitute for shaving cream to prevents razor burn.</li>\r\n	<li><strong>For acne-free skin:</strong>&nbsp;Mix 20 drops of tea tree essential oil with 15 drops of lavender essential oil, 15 frankincense essential oil and 10 ml jojoba oil and store in an amber bottle and use every night.</li>\r\n	<li><strong>Lip scrub:</strong>&nbsp;You can make a lip scrub with jojoba oil by mixing it with 1 tbsp brown sugar, 5 drops peppermint essential oil, 1 tbsp pure honey.</li>\r\n</ul>', 13),
(18, 'Ingredients', '<p>Shea Butter And Organic Cold Pressed Sweet Almond Oil. Dm-Water, Caprylic Capric Triglyceride, Glycerine, Rosehip Oil, Emulsifying Wax, Organic Cold Pressed Sweet Almond Oil Stearic Acid, Cetyl Alcholo, Soidium Pca, Panthenol,Glycerin, Sodium Hyaluronate, L-Proline, Hydroxproline, Fragrance Phenoxyethanol, Benzoic Acid, Undecylenoyl Glycine, Capryloyl Glycine, Triethanolamine, Vit.E. Acetate And Avocado Oil.</p>\r\n\r\n<p>&nbsp;</p>', 15),
(19, 'How To Use', '<p>Take one to two pumps of lotion on your palm and apply it on the entire body. Massage it for a few minutes on your skin to help it penetrate. For best results, use daily.</p>\r\n\r\n<p>&nbsp;</p>', 15),
(20, 'Ingredients', '<p><strong>Ceramide Barrier Repair Deep Nourish Day Moisturizer For Normal To Dry Skin With SPF 15&nbsp;</strong></p>\r\n\r\n<p>Purified Water, Cetyl Alcohol, Ethylhexyl Methoxycinnamate, Witch Hazel Extract, Phenoxyethanol, Glycerin, Ceramide NP, Ceramide AP, Ceramide EOP, Carbomer, Glyceryl Stearate, Butyl Methoxydibenzoylmethane, Polyethylene Glycol Stearate, Betaine, Propanediol, Phytosqualane, Oat Bran Extract, Shea Butter, Methylpropanediol, Benzophenone-3, Stearyl Alcohol, Triethanolamine, Olea Europaea (Olive) Fruit Oil, Olea Europaea (Olive) Leaf Extract, Olea Europaea (Olive) Fruit Extract, Phospholipids, Ethylhexylglycerin, Sodium Gluconate, Centella Asiatica Leaves, Glyceryl Glucoside, 1,3 Butylene Glycol, Propylene Glycol, Sodium Lauroyl Lactylate, Sodium Benzoate, Phytosphingosine, Cholesterol, Xanthan Gum</p>\r\n\r\n<p>&nbsp;</p>', 16);

-- --------------------------------------------------------

--
-- Table structure for table `main_productimage`
--

CREATE TABLE `main_productimage` (
  `id` bigint(20) NOT NULL,
  `image` varchar(100) NOT NULL,
  `order` int(11) NOT NULL DEFAULT 0,
  `alt_text` varchar(255) NOT NULL,
  `product_id` bigint(20) NOT NULL,
  `media_type` varchar(10) NOT NULL DEFAULT 'image'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `main_productimage`
--

INSERT INTO `main_productimage` (`id`, `image`, `order`, `alt_text`, `product_id`, `media_type`) VALUES
(1, 'products/2025/12/19/a4bed56NYKAC00001686_1.avif', 0, 'Blur away pesky pores and unwanted', 1, 'image'),
(2, 'products/2025/12/19/a4bed56NYKAC00001686_3.avif', 0, 'Blur away pesky pores and unwanted', 1, 'image'),
(3, 'products/2025/12/19/a4bed56NYKAC00001686_5.avif', 0, 'Blur away pesky pores and unwanted', 1, 'image'),
(4, 'products/2025/12/19/a4bed56NYKAC00001686_2.avif', 0, 'Blur away pesky pores and unwanted', 1, 'image'),
(5, 'products/2025/12/19/Lotion-with-Licorice-Front-scaled.jpg', 0, 'Body Lotion', 2, 'image'),
(6, 'products/2025/12/19/Lotion-with-Licorice-Back-2048x2048.jpg', 0, 'Body Lotion', 2, 'image'),
(7, 'products/2025/12/19/LOTION-WITH-LICORICE-KEY-POINTS.png', 0, 'Body Lotion', 2, 'image'),
(8, 'products/2025/12/19/Onion-Hair-Oil-with-Onion-and-Fenugreek.png', 0, '', 4, 'image'),
(9, 'products/2025/12/19/Onion-Hair-Oil-Side-scaled.jpg', 0, '', 4, 'image'),
(10, 'products/2025/12/19/Onion-Hair-Oil-Side-scaled_o6mcJbz.jpg', 0, '', 4, 'image'),
(11, 'products/2025/12/19/ONION-HAIR-SHAMPOO-KEY-POINTS.png', 0, '', 5, 'image'),
(12, 'products/2025/12/19/Onion-Hair-Shampoo-Front-scaled.jpg', 0, '', 5, 'image'),
(13, 'products/2025/12/19/16e91fe651986210541_1.avif', 0, '', 6, 'image'),
(14, 'products/2025/12/19/16e91fe651986210541_3.avif', 0, '', 6, 'image'),
(15, 'products/2025/12/19/597c9c5651986971961_a1.avif', 0, '', 7, 'image'),
(16, 'products/2025/12/19/771dede651986971961_3.avif', 0, '', 7, 'image'),
(17, 'products/2025/12/19/cruelty.avif', 0, '', 7, 'image'),
(18, 'products/2025/12/19/99ca87fNYKAC00002725_1.avif', 0, '', 8, 'image'),
(19, 'products/2025/12/19/99ca87fNYKAC00002725_2.avif', 0, '', 8, 'image'),
(20, 'products/2025/12/19/0076e1eNYXPR00000181_1.avif', 0, '', 9, 'image'),
(21, 'products/2025/12/19/0076e1eNYXPR00000181_1_1.avif', 0, '', 9, 'image'),
(22, 'products/2025/12/19/bf16427NYXPR00000672_1.avif', 0, '', 10, 'image'),
(23, 'products/2025/12/19/bf16427NYXPR00000672_2.avif', 0, '', 10, 'image'),
(24, 'products/2025/12/22/Ghrit-Kumari-Hair-Oil-Front-1900X1900.png', 0, '', 3, 'image'),
(25, 'products/2025/12/22/Ghrit-Kumari-Hair-Oil-Points.png', 0, '', 3, 'image'),
(26, 'products/2025/12/22/Ghrit-Kumari-Hair-Oil-Vector.png', 0, '', 3, 'image'),
(27, 'products/2025/12/22/994a850NYKAB00000184_1.avif', 0, '', 11, 'image'),
(28, 'products/2025/12/22/994a850NYKAB00000184_2.avif', 0, '', 11, 'image'),
(29, 'products/2025/12/22/994a850NYKAB00000184_4.avif', 0, '', 11, 'image'),
(30, 'products/2025/12/22/12daef48904245702076_1.avif', 0, '', 12, 'image'),
(31, 'products/2025/12/22/12daef48904245702076_3.avif', 0, '', 12, 'image'),
(32, 'products/2025/12/22/12daef48904245702076_4.avif', 0, '', 12, 'image'),
(33, 'products/2025/12/22/12daef48904245702076_1_1.avif', 0, '', 12, 'image'),
(34, 'products/2025/12/22/8904245705350_1_2.avif', 0, '', 13, 'image'),
(35, 'products/2025/12/22/8904245705350_2.avif', 0, '', 13, 'image'),
(36, 'products/2025/12/22/8904245705350_3.avif', 0, '', 13, 'image'),
(37, 'products/2025/12/22/8904245705350_goo.avif', 0, '', 13, 'image'),
(38, 'products/2025/12/22/3f4097f8906056670285_2B.avif', 0, '', 14, 'image'),
(39, 'products/2025/12/22/3f4097f8906056670285_1B.avif', 0, '', 14, 'image'),
(40, 'products/2025/12/22/3f4097f8906056670285_7B.avif', 0, '', 14, 'image'),
(41, 'products/2025/12/22/3f4097f8906056670285_5B.avif', 0, '', 14, 'image'),
(42, 'products/2025/12/22/44532618906056679257_0.avif', 0, '', 15, 'image'),
(43, 'products/2025/12/22/44532618906056679257_1.avif', 0, '', 15, 'image'),
(44, 'products/2025/12/22/44532618906056679257_2.avif', 0, '', 15, 'image'),
(45, 'products/2025/12/22/44532618906056679257_3.avif', 0, '', 15, 'image'),
(46, 'products/2025/12/22/6d6130dNYKAE00000040_1.avif', 0, 'Nykaa SkinRX', 16, 'image'),
(47, 'products/2025/12/22/6d6130dNYKAE00000040_2.avif', 0, 'Nykaa SkinRX', 16, 'image'),
(48, 'products/2025/12/22/6d6130dNYKAE00000040_4.avif', 0, 'Nykaa SkinRX', 16, 'image'),
(49, 'products/2025/12/22/6d6130dNYKAE00000040_6.avif', 0, 'Nykaa SkinRX', 16, 'image');

-- --------------------------------------------------------

--
-- Table structure for table `main_productvariation`
--

CREATE TABLE `main_productvariation` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `price_modifier` decimal(10,2) DEFAULT NULL,
  `stock` int(10) UNSIGNED DEFAULT NULL,
  `product_id` bigint(20) NOT NULL,
  `quantity` varchar(100) NOT NULL,
  `unit` varchar(50) DEFAULT NULL,
  `is_sku_code` varchar(100) DEFAULT NULL COMMENT 'Is SKU Code',
  `color_code` varchar(7) DEFAULT NULL COMMENT 'Color Code',
  `offerprice` decimal(10,2) DEFAULT 0.00 COMMENT 'Offer Price (INR)',
  `slug` varchar(200) DEFAULT NULL COMMENT 'Slug'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `main_productvariation`
--

INSERT INTO `main_productvariation` (`id`, `name`, `price_modifier`, `stock`, `product_id`, `quantity`, `unit`, `is_sku_code`, `color_code`, `offerprice`, `slug`) VALUES
(1, 'skin Bowls & Bonboniers', 150.00, 100, 15, '100', 'ml', 'skin100ml', '#ffb8b8', 120.00, 'skin-bowls-bonboniers'),
(2, 'Nykaa SkinRX Ceramide Barrier Repair Face Moisturizer with SPF 14', 300.00, 20, 16, '200', 'ml', 'nyfac-10', '#000000', 250.00, 'nykaa-skinrx-ceramide-barrier-repair-face-moisturizer-with-spf-14'),
(3, 'MOD Ghrit Kumari Hair Oil- hair growth with 100% Aloe Vera juice 200', 470.00, NULL, 3, '200', 'ml', 'GKHO-300', '#000000', 430.00, 'mod-ghrit-kumari-hair-oil-hair-growth-with-100-aloe-vera-juice-200'),
(4, 'Nyassa Under The Ocean 150g Bath Salts', 360.00, 20, 14, '120', 'g', 'nyksal-3', '#000000', 320.00, 'nyassa-under-the-ocean-150g-bath-salts'),
(5, 'Nykaa Naturals Tea Tree Essential Oil For Acne & Hair Fall Control Solution', 245.00, 30, 12, '5', 'ml', 'nyhairoil-3', '#000000', 220.00, 'nykaa-naturals-tea-tree-essential-oil-for-acne-hair-fall-control-solution'),
(6, 'Nykaa Naturals Tea Tree & Neem Purifying & Hydrating Gel - Controls Oils, Acne & Uneven', 149.00, 100, 11, '50', 'g', 'nyfac-5.1', '#000000', 100.00, 'nykaa-naturals-tea-tree-neem-purifying-hydrating-gel-controls-oils-acne-uneven'),
(7, 'NYX Professional Makeup Buttermelt Glaze Soft Glow Skin Tint + SPF 20', 1305.00, 30, 10, '20', 'ml', 'nyfac-4.1', '#000000', 1205.00, 'nyx-professional-makeup-buttermelt-glaze-soft-glow-skin-tint-spf-20'),
(8, 'NYX Professional Makeup Bare With Me Serum And Calm Concealer', 949.00, 88, 9, '8.5', 'ml', 'nyfac-3.1', '#000000', 900.00, 'nyx-professional-makeup-bare-with-me-serum-and-calm-concealer');

-- --------------------------------------------------------

--
-- Table structure for table `main_subcategory`
--

CREATE TABLE `main_subcategory` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `image` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `order` int(11) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `category_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `main_subcategory`
--

INSERT INTO `main_subcategory` (`id`, `name`, `slug`, `image`, `is_active`, `order`, `created`, `updated`, `category_id`) VALUES
(1, 'Foundation', 'foundation', 'subcategories/2025/12/19/mackup.webp', 1, 1, '2025-12-19 12:05:50.982378', '2025-12-19 12:05:50.982378', 1),
(2, 'Loose Powder', 'loose-powder', 'subcategories/2025/12/19/4.webp', 1, 2, '2025-12-19 12:07:02.593862', '2025-12-19 12:07:02.593862', 1),
(3, 'Body Lotion', 'body-lotion', '', 1, NULL, '2025-12-19 12:35:53.837465', '2025-12-19 12:35:53.837499', 2),
(4, 'Hair oil', 'hair-oil', '', 1, NULL, '2025-12-19 12:58:59.925675', '2025-12-19 12:58:59.925695', 3),
(5, 'Hair Shampoo', 'hair-shampoo', '', 1, NULL, '2025-12-19 13:08:48.212069', '2025-12-19 13:08:48.212086', 3),
(6, 'Eyes', 'eyes', '', 1, NULL, '2025-12-19 13:13:57.148972', '2025-12-19 13:13:57.148992', 1),
(7, 'Face', 'face', '', 1, NULL, '2025-12-19 16:57:31.376419', '2025-12-19 16:57:31.376443', 1),
(8, 'Hair Mask', 'hair-mask', '', 1, NULL, '2025-12-22 17:12:45.280517', '2025-12-22 17:12:45.280535', 3),
(9, 'Hair Serum', 'hair-serum', '', 1, NULL, '2025-12-22 17:13:18.530729', '2025-12-22 17:13:18.530748', 3),
(10, 'Hair Conditioner', 'hair-conditioner', '', 1, NULL, '2025-12-22 17:13:41.448795', '2025-12-22 17:13:41.448810', 3),
(11, 'Day Cream', 'day-cream', 'subcategories/2025/12/22/1.webp', 1, NULL, '2025-12-22 17:14:10.721387', '2025-12-22 17:14:10.721407', 5),
(12, 'Night Cream', 'night-cream', 'subcategories/2025/12/22/1.webp', 1, NULL, '2025-12-22 17:15:15.761558', '2025-12-22 17:15:15.761580', 5),
(13, 'Under Eye Cream', 'under-eye-cream', '', 1, NULL, '2025-12-22 17:15:27.742003', '2025-12-22 17:15:27.742020', 5),
(14, 'Face Wash', 'face-wash', '', 1, NULL, '2025-12-22 17:15:44.888295', '2025-12-22 17:15:44.888310', 5),
(15, 'face Serum', 'face-serum', '', 1, NULL, '2025-12-22 17:16:16.811292', '2025-12-22 17:16:16.811308', 5),
(16, 'Cleansers', 'cleansers', '', 1, NULL, '2025-12-22 17:16:31.172641', '2025-12-22 17:16:31.172664', 5),
(17, 'Sunscreen Lotion', 'sunscreen-lotion', '', 1, NULL, '2025-12-22 17:16:43.574778', '2025-12-22 17:16:43.574803', 5),
(18, 'Face Pack', 'face-pack', '', 1, NULL, '2025-12-22 17:17:01.909349', '2025-12-22 17:17:01.909368', 5),
(19, 'face Scrubs', 'face-scrubs', '', 1, NULL, '2025-12-22 17:17:25.500280', '2025-12-22 17:17:25.500304', 5),
(20, 'Face Oil', 'face-oil', '', 1, NULL, '2025-12-22 17:17:37.420403', '2025-12-22 17:17:37.420423', 5),
(21, 'Facial Kit', 'facial-kit', '', 1, NULL, '2025-12-22 17:17:51.089989', '2025-12-22 17:17:51.090007', 5),
(22, 'Rose Water', 'rose-water', '', 1, NULL, '2025-12-22 17:18:11.291113', '2025-12-22 17:18:11.291131', 5),
(23, 'Heel Care Cream', 'heel-care-cream', '', 1, NULL, '2025-12-22 17:20:01.173356', '2025-12-22 17:20:01.173385', 4),
(24, 'Lipstick – Liquid', 'lipstick-liquid', '', 1, NULL, '2025-12-22 17:21:46.297643', '2025-12-22 17:21:46.297663', 1),
(25, 'Eye Liner', 'eye-liner', '', 1, NULL, '2025-12-22 17:22:04.490805', '2025-12-22 17:22:04.490825', 1),
(26, 'Mascara', 'mascara', '', 1, NULL, '2025-12-22 17:22:18.848957', '2025-12-22 17:22:18.848977', 1),
(27, 'Liquid Sindoor', 'liquid-sindoor', '', 1, NULL, '2025-12-22 17:24:32.170227', '2025-12-22 17:24:32.170249', 1),
(28, 'Lipstick – Stick', 'lipstick-stick', '', 1, NULL, '2025-12-22 17:24:51.615802', '2025-12-22 17:24:51.615831', 1),
(29, 'Soap', 'soap', '', 1, NULL, '2025-12-22 17:29:07.308593', '2025-12-22 17:29:07.308613', 2),
(30, 'Body Wash', 'body-wash', '', 1, NULL, '2025-12-22 17:29:20.620263', '2025-12-22 17:29:20.620283', 2),
(31, 'Massage Oil', 'massage-oil', '', 1, NULL, '2025-12-22 17:29:34.788490', '2025-12-22 17:29:34.788508', 2),
(32, 'Bath Salt', 'bath-salt', '', 1, NULL, '2025-12-22 17:29:51.990213', '2025-12-22 17:29:51.990228', 2),
(33, 'Body Gel', 'body-gel', '', 1, NULL, '2025-12-22 17:30:12.710050', '2025-12-22 17:30:12.710073', 2);

-- --------------------------------------------------------

--
-- Table structure for table `main_useraddress`
--

CREATE TABLE `main_useraddress` (
  `id` bigint(20) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `address_line1` varchar(255) NOT NULL,
  `address_line2` varchar(255) DEFAULT NULL,
  `city` varchar(100) NOT NULL,
  `state` varchar(100) NOT NULL,
  `zip_code` varchar(10) NOT NULL,
  `country` varchar(100) NOT NULL,
  `is_default` tinyint(1) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `main_useraddress`
--

INSERT INTO `main_useraddress` (`id`, `full_name`, `phone`, `address_line1`, `address_line2`, `city`, `state`, `zip_code`, `country`, `is_default`, `created`, `updated`, `user_id`) VALUES
(1, 'Swapnil', '7987947020', 'B/13 90 quater', 'Shakti nagar', 'Jabalpur', 'MP', '482001', 'India', 0, '2026-01-10 10:31:42.450559', '2026-01-10 10:31:42.450592', 2);

-- --------------------------------------------------------

--
-- Table structure for table `offers`
--

CREATE TABLE `offers` (
  `id` bigint(20) NOT NULL,
  `offer_name` varchar(50) NOT NULL,
  `page_position` varchar(50) NOT NULL,
  `offer_title` varchar(150) NOT NULL,
  `offer_slug` varchar(180) NOT NULL,
  `offer_description` longtext DEFAULT NULL,
  `offer_image` varchar(100) NOT NULL,
  `meta_title` varchar(160) NOT NULL,
  `meta_description` varchar(255) NOT NULL,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `order` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `offers`
--

INSERT INTO `offers` (`id`, `offer_name`, `page_position`, `offer_title`, `offer_slug`, `offer_description`, `offer_image`, `meta_title`, `meta_description`, `start_date`, `end_date`, `is_active`, `created_at`, `order`) VALUES
(2, 'HOT_PRODUCT', 'HOME_TOP', 'Hot Product Collections', 'hot-product-collections', 'Premium quality products ka curated collection.', 'offers/4.jpg', 'Premium quality products ka curated collection.', 'Premium quality products ka curated collection.', '2026-01-17 16:47:33.000000', '2026-05-17 16:47:35.000000', 1, '2026-01-17 16:47:59.629950', 3),
(3, 'NEW_LAUNCH', 'HOME_TOP', 'New Launch Product', 'new-launch-product', 'Latest innovation ke saath launch hua naya product.', 'offers/4_aSQwlJG.jpg', 'Latest innovation ke saath launch hua naya product.', 'Latest innovation ke saath launch hua naya product, jo modern needs, premium quality aur best performance deliver karta hai.', '2026-01-17 16:49:55.000000', '2026-05-17 16:49:57.000000', 1, '2026-01-17 16:50:14.852650', 2),
(4, 'MY_SUNDAY', 'HOME_TOP', 'My Sunday Offers', 'my-sunday-offers', 'Sunday special deals aur exclusive discounts.', 'offers/1_tPgp0K1.jpg', 'Sunday special deals aur exclusive discounts.', 'Sunday special deals aur exclusive discounts.', '2026-01-17 17:55:06.000000', '2026-05-17 17:55:08.000000', 1, '2026-01-17 17:55:33.416362', 1);

-- --------------------------------------------------------

--
-- Table structure for table `offer_products`
--

CREATE TABLE `offer_products` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `offer_id` bigint(20) NOT NULL,
  `product_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `cms_blog`
--
ALTER TABLE `cms_blog`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `cms_cms`
--
ALTER TABLE `cms_cms`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `cms_profile_setting`
--
ALTER TABLE `cms_profile_setting`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `cms_slider`
--
ALTER TABLE `cms_slider`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `main_brand`
--
ALTER TABLE `main_brand`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `main_category`
--
ALTER TABLE `main_category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `main_coupon`
--
ALTER TABLE `main_coupon`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `main_coupon_valid_products`
--
ALTER TABLE `main_coupon_valid_products`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `main_coupon_valid_products_coupon_id_product_id_0ce6682f_uniq` (`coupon_id`,`product_id`);

--
-- Indexes for table `main_customuser`
--
ALTER TABLE `main_customuser`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `main_order`
--
ALTER TABLE `main_order`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `main_order_coupons`
--
ALTER TABLE `main_order_coupons`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `main_order_coupons_order_id_coupon_id_9c2410e1_uniq` (`order_id`,`coupon_id`);

--
-- Indexes for table `main_payment`
--
ALTER TABLE `main_payment`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `main_product`
--
ALTER TABLE `main_product`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `main_subcategory`
--
ALTER TABLE `main_subcategory`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `main_useraddress`
--
ALTER TABLE `main_useraddress`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_useraddress_user_id_b8945ef0_fk_main_customuser_id` (`user_id`);

--
-- Indexes for table `offers`
--
ALTER TABLE `offers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `offer_slug` (`offer_slug`);

--
-- Indexes for table `offer_products`
--
ALTER TABLE `offer_products`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `offer_products_offer_id_product_id_a78674f8_uniq` (`offer_id`,`product_id`),
  ADD KEY `offer_products_product_id_e63a77e9_fk_main_product_id` (`product_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=117;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `cms_blog`
--
ALTER TABLE `cms_blog`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `cms_cms`
--
ALTER TABLE `cms_cms`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `cms_profile_setting`
--
ALTER TABLE `cms_profile_setting`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `cms_slider`
--
ALTER TABLE `cms_slider`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=135;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=91;

--
-- AUTO_INCREMENT for table `main_brand`
--
ALTER TABLE `main_brand`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `main_category`
--
ALTER TABLE `main_category`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `main_coupon`
--
ALTER TABLE `main_coupon`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `main_coupon_valid_products`
--
ALTER TABLE `main_coupon_valid_products`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `main_customuser`
--
ALTER TABLE `main_customuser`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `main_order`
--
ALTER TABLE `main_order`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `main_order_coupons`
--
ALTER TABLE `main_order_coupons`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `main_payment`
--
ALTER TABLE `main_payment`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `main_product`
--
ALTER TABLE `main_product`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `main_subcategory`
--
ALTER TABLE `main_subcategory`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `main_useraddress`
--
ALTER TABLE `main_useraddress`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `offers`
--
ALTER TABLE `offers`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `offer_products`
--
ALTER TABLE `offer_products`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `offer_products`
--
ALTER TABLE `offer_products`
  ADD CONSTRAINT `offer_products_offer_id_43351a67_fk_offers_id` FOREIGN KEY (`offer_id`) REFERENCES `offers` (`id`),
  ADD CONSTRAINT `offer_products_product_id_e63a77e9_fk_main_product_id` FOREIGN KEY (`product_id`) REFERENCES `main_product` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
