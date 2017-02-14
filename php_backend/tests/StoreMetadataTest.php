<?php

require_once "src/QueryBuilder.php";
require_once "src/UploadProcessor.php";
require_once "src/MuBench/Misuse.php";
require_once "DatabaseTestCase.php";

use MuBench\Misuse;

class StoreMetadataTest extends DatabaseTestCase
{
    function test_store_metadata()
    {
        $queryBuilder = new QueryBuilder($this->pdo, $this->logger);
        $upload_processor = new UploadProcessor($this->db, $queryBuilder, $this->logger);

        $data = json_decode($this->metadata_json);
        $findings = json_decode($this->finding_json);

        $upload_processor->processData('ex1', $findings, $findings->{'potential_hits'});
        $upload_processor->processMetaData($data);

        $detector = $this->db->getDetector('-d-');
        $runs = $this->db->getRuns($detector, 'ex1');

        $expected_run = [
            "exp" => "ex1",
            "project" => "-p-",
            "version" => "-v-",
            "result" => "success",
            "runtime" => "42.1",
            "number_of_findings" => "23",
            "detector" => "detector_1",
            "misuses" => [
                new Misuse(
                    [
                    'misuse' => '-m-',
                    'project' => '-p-',
                    'version' => '-v-',
                    'description' => '-desc-',
                    'fix_description' => '-fix-desc-',
                    'violation_types' => 'superfluous/condition/null_check',
                    'file' => '-f-',
                    'method' => '-method-',
                    'diff_url' => '-diff-',
                    'snippets' => [0 => ['line' => '273', 'snippet' => '-code-']],
                    'patterns' => [0 => ['name' => '-p-id-', 'code' => '-pattern-code-','line' => '1']]
                    ],
                    [
                        [
                            'exp' => 'ex1',
                            'project' => '-p-',
                            'version' => '-v-',
                            'misuse' => '-m-',
                            'rank' => '0',
                            'custom1' => '-val1-',
                            'custom2' => '-val2-'
                        ]
                    ],
                    [])
            ]
        ];

        self::assertEquals([$expected_run], $runs);
    }

}