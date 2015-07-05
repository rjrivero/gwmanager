#!/usr/bin/env node

var format   = require('string-format');
var pkgcloud = require('pkgcloud');

var argv = require('yargs')
    .usage('Usage: $0 -u <username> [-p <password>] <auth_url>')
    .example('$0 -u test:tester -p testing "http://localhost:8080"')
    .demand(1)
    .option('u', {
        alias: 'username',
        demand: true,
        describe: 'Username',
        type: 'string'
    })
    .nargs('u', 1)
    .option('p', {
        alias: 'password',
        demand: false,
        describe: 'Password',
        type: 'string'
    })
    .nargs('p', 1)
    .version(function() {
        return require('./package').version;
    })
    .showHelpOnFail(true, "-h / --help for further options")
    .argv
    
// See https://www.npmjs.com/package/string-format
if (!String.prototype.format) {
    format.extend(String.prototype);
}

// List all files in a container
function listFiles(client, container) {
    client.getFiles(container, function(err, files) {
        if (err) {
            console.log("Error fetching files from {0}: {1}".format(container.name, err));
            return;
        }
        console.log(container.name.concat(":"));
        files.forEach(function(file, index, array) {
            console.log("    {name} ({size} bytes)".format(file));
        });
    });
}

// List all containers
function listContainers(client) {
    client.getContainers(function(err, containers) {
        if (err) {
            console.log("Error fetching containers: ".concat(err));
            return;
        }
        containers.forEach(function(container, index, array) {
            listFiles(client, container);
        });
    });
}

// List all files and containers
function main(argv) {
    // See https://github.com/pkgcloud/pkgcloud/issues/311
    var client = pkgcloud.storage.createClient({
        provider: 'openstack',
        username: argv.u,
        password: argv.p,
        authUrl: argv._[0],
        version: 1,
        useServiceCatalog: false
    });
    listContainers(client)
}

// run
if (!argv.p) {
    var read = require('read')
    read({ prompt: "Password: ", silent: true, replace: '*' }, function(err, password, isDefault) {
        if (err) {
            console.log("Could not read password: ".concat(err));
            process.exit(-1);
        }
        argv.p = password;
        main(argv);
    });
}
else {
    main(argv);
}
