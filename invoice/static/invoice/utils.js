
export async function OPTIONS(url) {
    const response = await fetch(url, {method: "OPTIONS"});
    const data = await response.json();
    return data;
}
export async function GET(url) {
    const response = await fetch(url);
    const data = await response.json();
    return data;
}
export async function POST(url, jsonData) {
    const response = await fetch(url, {method: "POST", body: JSON.stringify(jsonData)});
    const data = await response.json();
    return data;
}
export async function PUT(url, jsonData) {
    const response = await fetch(url, {method: "PUT", body: JSON.stringify(jsonData)});
    const data = await response.json();
    return data;
}
export async function PATCH(url, jsonData) {
    const response = await fetch(url, {method: "PATCH", body: JSON.stringify(jsonData)});
    const data = await response.json();
    return data;
}
export async function DELETE(url) {
    const response = await fetch(url, {method: "DELETE"});
    const data = await response.json();
    return data;
}




export function textToHTML(html) {
    const template = document.createElement("template");
    template.innerHTML = html;
    return template.content;
}
