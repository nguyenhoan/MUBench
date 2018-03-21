<?php
return [
    'settings' => [
        'displayErrorDetails' => false, // set to false in production
        'addContentLengthHeader' => false, // Allow the web server to send the content-length header

        'db' => [
            'driver' => 'sqlite',
            'host' => 'localhost',
            'database' => __DIR__ . '/test.sqlite',
            'username' => 'admin',
            'password' => 'admin',
            'charset'   => 'utf8',
            'collation' => 'utf8_unicode_ci',
            'prefix'    => '',
        ],

        // Monolog settings
        'logger' => [
            'name' => 'mubench',
            'path' => __DIR__ . '/logs/app.log',
            'level' => \Monolog\Logger::DEBUG,
        ],

        'site_base_url' => '/',
        'upload' => "./upload",
        'default_ex2_review_size' => '20'
    ],
    'users' => [
        "admin" => "pass"
    ],
    'blind_mode' => [
        'enabled' => false,
        'detector_blind_names' => []
    ]
];
