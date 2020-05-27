// University of Melbourne 
// COMP90024 - Team52
// Name of contributors and student id:
// * Edward Formainir: 1073708
// * Niloy Sarkar: 991245
// * Marc Girard: 1155873
// * Runqi Zhu: 793024

module.exports = function (grunt) {
  grunt
    .initConfig({
      "couch-compile": {
        dbs: {
          files: {
            "/tmp/steamtest.json": "/location"
          }
        }
      },
      "couch-push": {
        options: {
          user: process.env.user,
          pass: process.env.pass
        },
        steamtest: {
        }
      }
    });

  grunt.config.set(`couch-push.steamtest.files.http://172\\.26\\.134\\.6:5984/${process.env.dbname}`, "/tmp/steamtest.json");
console.log(JSON.stringify(grunt.config.get()));
  grunt.loadNpmTasks("grunt-couch");
};
