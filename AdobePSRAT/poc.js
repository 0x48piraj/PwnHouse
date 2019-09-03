const core = require("generator-core/lib/generator")
const creds = {
    host: '10.163.3.220',
    password: '123456',
    port: 49494
}
const generator = core.createGenerator({ createLogger: () => console})
generator.start(creds).done(() => {
    generator.evaluateJSXString('alert(1);').then(() => generator.shutdown())
})