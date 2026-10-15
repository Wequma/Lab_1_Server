<?php

declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

const DATA_FILE = __DIR__ . DIRECTORY_SEPARATOR . 'data.json';

/** Відправляє JSON-відповідь і завершує виконання API. */
function respond(mixed $data, int $statusCode = 200): never
{
    http_response_code($statusCode);
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    header('Allow: GET');
    respond(['error' => 'Метод не підтримується. Використовуйте GET.'], 405);
}

if (!is_file(DATA_FILE)) {
    respond(['error' => 'Файл з даними не знайдено.'], 500);
}

$json = file_get_contents(DATA_FILE);
$data = json_decode($json ?: '', true);

if (!is_array($data) || !isset($data['products']) || !is_array($data['products'])) {
    respond(['error' => 'Некоректний формат data.json.'], 500);
}

$products = $data['products'];

// GET /index.php?id=1 — повернути один товар.
if (isset($_GET['id'])) {
    $id = filter_var($_GET['id'], FILTER_VALIDATE_INT);

    if ($id === false || $id < 1) {
        respond(['error' => 'Параметр id має бути додатним числом.'], 400);
    }

    foreach ($products as $product) {
        if (($product['id'] ?? null) === $id) {
            respond($product);
        }
    }

    respond(['error' => 'Товар не знайдено.'], 404);
}

// GET /index.php — повернути всі товари.
respond([
    'count' => count($products),
    'products' => $products,
]);
